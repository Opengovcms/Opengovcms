from zope.interface import Interface
from zope import schema
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn
from i18n import MessageFactory as _


class IBrowserLayer(Interface):
    """ browser layer for the policy package  """


class ISiteSettings(Interface):
    """ Global site specific settings """

    address = schema.Text(
        title=_(u"Address"),
        description=_(u"This text will be used in the footer for "
                      u"address information."),
        required=False,
        default=u'',
    )


class ISearchPortletManager(IPortletManager, IColumn):
    """
    """


class ISearchPortlets(ISearchPortletManager):
    """
    For the portlet manager in the search.
    """