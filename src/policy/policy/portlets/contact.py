from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from AccessControl import getSecurityManager
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from policy.i18n import MessageFactory as _

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")

class IContact(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)

    target = schema.Choice(
        title=_(u"Target person"),
        description=_(u"Find the person to display"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': 'Person'},
            default_query='path:'))


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IContact)

    header = u""
    target = None

    def __init__(self, header=u"", target=None):
        self.header = header
        self.target = target

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return self.header or _(u"Contact")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('contact.pt')

    @property
    def available(self):
        if self.person():
            return True
        return False

    def url(self):
        person = self.person()
        if person is None:
            return None
        else:
            return person.absolute_url()

    @memoize
    def person(self):
        path = self.data.target
        if not path:
            return None

        if path.startswith('/'):
            path = path[1:]

        if not path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(path, unicode):
            # restrictedTraverse accepts only strings
            path = str(path)

        result = portal.unrestrictedTraverse(path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result




class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IContact)
    form_fields['target'].custom_widget = UberSelectionWidget

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IContact)
    form_fields['target'].custom_widget = UberSelectionWidget

