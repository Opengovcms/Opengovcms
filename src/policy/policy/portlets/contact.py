from AccessControl import getSecurityManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.app.portlets.browser import z3cformhelper
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from policy.i18n import MessageFactory as _
from policy.content.person import IPerson
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.component import getMultiAdapter
from z3c.form import field
from zope.interface import implements

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

    target = RelationChoice(
        title=_(u"Target person"),
        description=_(u"Find the person to display"),
        required=True,
        source=ObjPathSourceBinder(
            object_provides=IPerson.__identifier__
        ),
    )


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
        result = self.data.target.to_object
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result


class AddForm(z3cformhelper.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    fields = field.Fields(IContact)

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    fields = field.Fields(IContact)
