from plone.app.layout.viewlets.common import GlobalSectionsViewlet as ViewletBase
from plone.app.layout.viewlets.content import DocumentBylineViewlet as BylineBase
from plone.app.layout.navigation.defaultpage import getDefaultPage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from zope.component.hooks import getSite

from collective.panels.traversal import PanelManager
from plone.app.theming.utils import isThemeEnabled


class GlobalSectionsViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/sections.pt')

    @property
    def isThemeEnabled(self):
        return isThemeEnabled(self.request)

    def getItem(self, tab):
        site = getSite()
        context = aq_inner(self.context)
        if tab.get('available'):
            item = site
        else:
            item = site.restrictedTraverse(tab['id'])
        def_page = getDefaultPage(item)
        if def_page:
            item = item.restrictedTraverse(def_page)
        return item

    def getPanels(self, context):
        try:
            manager = PanelManager(context,
                                   self.request,
                                   context,
                                   "plone.portaltop"
                                   ).__of__(context)
            return tuple(manager)
        except TypeError:
            return tuple()

class DocumentBylineViewlet(BylineBase):
    index = ViewPageTemplateFile("templates/document_byline.pt")

    def show(self):
        is_portal_root = self.context_state.is_portal_root()
        context = aq_inner(self.context)
        try:
            manager = PanelManager(context,
                                   self.request,
                                   context,
                                   "plone.belowcontentbody"
                                   ).__of__(context)
            panels = len(tuple(manager)) > 0
        except:
            panels = False
        return not is_portal_root and not panels