from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlet.collection import PloneMessageFactory as _c
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.portlet.collection import collection
from plone.portlets.interfaces import IPortletDataProvider
from z3c.form import field
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implements
from policy.i18n import MessageFactory as _

COLLECTIONS = []

try:
    from plone.app.collection.interfaces import ICollection
    COLLECTIONS.append(ICollection.__identifier__)
except ImportError:
    pass

try:
    from plone.app.contenttypes.interfaces import ICollection
    COLLECTIONS.append(ICollection.__identifier__)
except ImportError:
    pass


class INews(IPortletDataProvider):
    """ """
    header = schema.TextLine(
        title=_c(u"Portlet header"),
        description=_c(u"Title of the rendered portlet"),
        required=True)

    target_collection = RelationChoice(
        title=_c(u"Target collection"),
        description=_c(u"Find the collection which provides the items to list"),
        required=True,
        source=ObjPathSourceBinder(
            object_provides=COLLECTIONS
        ),
    )

    limit = schema.Int(
        title=_c(u"Limit"),
        description=_c(u"Specify the maximum number of items to show in the "
                      u"portlet. Leave this blank to show all items."),
        required=False)

    show_more = schema.Bool(
        title=_c(u"Show more... link"),
        description=_c(u"If enabled, a more... link will appear in the footer "
                      u"of the portlet, linking to the underlying "
                      u"Collection."),
        required=True,
        default=True)

    show_more_text = schema.TextLine(
        title=_(u"Show more text"),
        description=_(u"Specify the text used in the show more-link"),
        required=False,
        default=u''
    )


class Assignment(collection.Assignment):
    """ """
    implements(collection.ICollection, INews)

    show_more_text = ""

    def __init__(self, **kwargs):
        self.show_more_text = kwargs['show_more_text']

        super(Assignment, self).__init__(**kwargs)


class Renderer(collection.Renderer):
    """ """
    _template = ViewPageTemplateFile('news.pt')
    render = _template


class AddForm(collection.AddForm):
    """ """

    fields = field.Fields(INews)
    
    label = _c(u"Add News Portlet")
    description = _c(u"This portlet displays recent News Items.")

    def create(self, data):
        return Assignment(**data)


class EditForm(collection.EditForm):
    """ """

    fields = field.Fields(INews)

    label = _c(u"Edit News Portlet")
    description = _c(u"This portlet displays recent News Items.")
