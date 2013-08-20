# encoding: utf-8
import logging

from z3c.form import field
from zope import schema
from zope.interface import implements
from zope.interface import Interface
from zope.app.form.interfaces import IWidgetInputError

from AccessControl import getSecurityManager
from Products.CMFCore import permissions

from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets.portlets import base
from plone.app.portlets.browser import z3cformhelper

from z3c.relationfield.schema import RelationChoice, RelationList
from z3c.relationfield.interfaces import IHasOutgoingRelations
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.textfield import RichText

from zope.component import adapts
from z3c.form.interfaces import IObjectFactory

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlet.static import PloneMessageFactory as _

logger = logging.getLogger('plone.portlet.static')

def isHttpURL(value):
    if value.startswith(u'http') or value.startswith(u'https'):
        return True
    else:
        raise UrlException

class UrlException(schema.ValidationError):
    __doc__ = u"""Please use a valid url like http://ploneconf2009.org"""
    implements(IWidgetInputError)


class IExternalLink(Interface):
    url = schema.ASCIILine(
        title=u"URL",
        default="http://",
        required=True,
        missing_value=u'',
        #constraint=isHttpURL,
        )
    description = schema.TextLine(
        title=u"Linktitel",
        required=False,
        )


class ExternalLink(object):
     implements(IExternalLink)

     def __init__(self, value):
         self.url = value["url"]
         self.description = value["description"]


class ExternalLinkFactory(object):
     adapts(Interface, Interface, Interface, Interface)
     implements(IObjectFactory)

     def __init__(self, context, request, form, widget):
         pass

     def __call__(self, value):
         return ExternalLink(value)


class ILinksListPortlet(IPortletDataProvider):
    """
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        required=False,
        )

    internal_links = RelationList(
        title=u'Interne links',
        default=[],
        value_type=RelationChoice(title=u"Internt link",
                      source=ObjPathSourceBinder()),
        required=False,
        )

    external_links = schema.List(
            value_type=schema.Object(
                    title=u'Link',
                    schema=IExternalLink),
            title=u"Eksterne links",
            required=False,
        )

    text = RichText(
            title=u"Tekst",
            required=False,
        )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ILinksListPortlet, IHasOutgoingRelations)

    header = u""
    internal_links = []
    external_links = []
    text = u""

    def __init__(self,
                 header=u"",
                 internal_links=[],
                 external_links=[],
                 text=u"",
                 ):
        self.header = header
        self.internal_links = internal_links
        self.external_links = external_links
        self.text = text

    @property
    def title(self):
        """
        """
        return self.header


class Renderer(base.Renderer):
    """
    """

    render = ViewPageTemplateFile('links_list_portlet.pt')

    @property
    @memoize
    def links(self):
        """
        """
        result = []
        if self.data.internal_links:
            for ref in self.data.internal_links:
                if ref is not None:
                    obj = ref.to_object
                    if obj:
                        if getSecurityManager().checkPermission(permissions.View, obj):
                            result.append({'link_type':'internal',
                                           'portal_type':obj.portal_type,
                                           'url':obj.absolute_url(),
                                           'description':obj.Title(),
                                           })
        if self.data.external_links:
            for link in self.data.external_links:
                if link.url and link.url != IExternalLink['url'].default:
                    result.append({'link_type':'external',
                                   'portal_type':None,
                                   'url':link.url,
                                   'description':link.description,
                                   })
        return result

    @property
    def available(self):
        """
        """
        return True


class AddForm(z3cformhelper.AddForm):
    """
    """
    fields = field.Fields(ILinksListPortlet)
    label = u"Tilføj linksliste-portlet"

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):
    """
    """
    fields = field.Fields(ILinksListPortlet)
    label = u"Rediger linksliste-portlet"

