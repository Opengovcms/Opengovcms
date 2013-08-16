from plone.app.portlets.portlets.navigation import Renderer, INavigationPortlet, getRootPath

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize
from Acquisition import aq_inner, aq_base, aq_parent
from zope.component import adapts, getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from Products.CMFPlone import utils
from zope.interface import implements, Interface
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy


class IPolicyNavtreeStrategy(INavtreeStrategy):
    pass

class IPolicyNavigationQueryBuilder(INavigationQueryBuilder):
    pass

class NavRenderer(Renderer):
    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('navigation_recurse.pt')

    @memoize
    def getNavTree(self, _marker=None):
        if _marker is None:
            _marker = []
        context = aq_inner(self.context)
        queryBuilder = getMultiAdapter((context, self.data), IPolicyNavigationQueryBuilder)
        strategy = getMultiAdapter((context, self.data), IPolicyNavtreeStrategy)
        return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)

    @memoize
    def getNavRootPath(self):
        currentFolderOnly = self.data.currentFolderOnly or \
                            self.properties.getProperty('currentFolderOnlyInNavtree', False)
        topLevel = self.properties.getProperty('topLevel', 0)
        return getRootPath(self.context, currentFolderOnly, topLevel, self.data.root)

    @property
    def available(self):

        rootpath = self.getNavRootPath()
        if rootpath is None:
            return False

        if self.data.bottomLevel < 0:
            return True

        tree = self.getNavTree()
        return len(tree['children']) > 0

class PolicyQueryBuilder(object):
    """Build a navtree query based on the settings in navtree_properties
    and those set on the portlet.
    """
    implements(IPolicyNavigationQueryBuilder)
    adapts(Interface, INavigationPortlet)

    def __init__(self, context, portlet):
        self.context = context
        self.portlet = portlet

        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')

        # Acquire a custom nav query if available
        customQuery = getattr(context, 'getCustomNavQuery', None)
        if customQuery is not None and utils.safe_callable(customQuery):
            query = customQuery()
        else:
            query = {}

        # Construct the path query

        rootPath = getNavigationRoot(context, relativeRoot=portlet.root)
        currentPath = '/'.join(context.getPhysicalPath())

        # If we are above the navigation root, a navtree query would return
        # nothing (since we explicitly start from the root always). Hence,
        # use a regular depth-1 query in this case.

        if currentPath != rootPath and not currentPath.startswith(rootPath + '/'):
            query['path'] = {'query': rootPath, 'depth': 1}
        else:
            query['path'] = {'query': currentPath, 'navtree': 1}

        topLevel = navtree_properties.getProperty('topLevel', 0)
        if topLevel and topLevel > 0:
            query['path']['navtree_start'] = topLevel + 1

        # XXX: It'd make sense to use 'depth' for bottomLevel, but it doesn't
        # seem to work with EPI.

        # Only list the applicable types
        query['portal_type'] = utils.typesToList(context)

        # Apply the desired sort
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        # Filter on workflow states, if enabled
        if navtree_properties.getProperty('enable_wf_state_filtering', False):
            query['review_state'] = navtree_properties.getProperty('wf_states_to_show', ())
        self.query = query

    def __call__(self):
        return self.query


class PolicyNavtreeStrategy(SitemapNavtreeStrategy):
    """The navtree strategy used for the default navigation portlet
    """
    implements(IPolicyNavtreeStrategy)
    adapts(Interface, INavigationPortlet)

    def __init__(self, context, portlet):
        SitemapNavtreeStrategy.__init__(self, context, portlet)
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')

        # XXX: We can't do this with a 'depth' query to EPI...
        self.bottomLevel = portlet.bottomLevel or \
                           navtree_properties.getProperty('bottomLevel', 0)

        currentFolderOnly = portlet.currentFolderOnly or \
            navtree_properties.getProperty('currentFolderOnlyInNavtree', False)

        topLevel = navtree_properties.getProperty('topLevel', 0)
        self.rootPath = getRootPath(context, currentFolderOnly, topLevel, portlet.root)

    def subtreeFilter(self, node):
        sitemapDecision = SitemapNavtreeStrategy.subtreeFilter(self, node)
        if sitemapDecision == False:
            return False
        depth = node.get('depth', 0)
        if depth > 0 and self.bottomLevel > 0 and depth >= self.bottomLevel:
            return False
        else:
            return True