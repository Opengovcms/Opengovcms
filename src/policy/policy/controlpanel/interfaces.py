from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import Interface, implements

from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.object import registerFactoryAdapter

from plone.registry.field import PersistentField
from plone.autoform import directives as form

from policy.i18n import MessageFactory as _

class PersistentObject(PersistentField, schema.Object):
    pass


class ISocialShareItem(Interface):

    priority = schema.Int(
            title=_("Priority"),
            required=False,
            default=99
    )
    
    url = schema.TextLine(
            title=_("URL"),
            required=True,
            default=u''
    )
    
    visible = schema.Bool(
        title=_("Visible"),
        required=False,
        default=False
    )

    icon_1 = schema.Bytes(
        title=_("Default icon"),
        required=False,
    )

    icon_2 = schema.Bytes(
        title=_("Rollover icon"),
        required=False,
    )

    dk_alt = schema.TextLine(
        title=_("Danish Alt"),
        required=True
    )

    uk_alt = schema.TextLine(
        title=_("English Alt"),
        required=True
    )


class SocialShareItem(object):
    implements(ISocialShareItem)

registerFactoryAdapter(ISocialShareItem, SocialShareItem)

class ISocialShareSettings(Interface):
    """ Settings for social share module"""

    social_share_items = schema.Tuple(
        title=_(u'Settings'), 
        value_type=PersistentObject(ISocialShareItem, title=u"Social share item"),
    )
    
    form.widget(style=RadioFieldWidget)
    style = schema.Choice(
        title=_("Style"),
        vocabulary=SimpleVocabulary([SimpleVocabulary.createTerm(1, '1', _(u'List')), 
                                     SimpleVocabulary.createTerm(2, '2', _(u'DropDown'))]),
        default=1
    )
    
    button_1 = schema.Bytes(
        title=_("Default button"),
        required=False,
    )

    button_2 = schema.Bytes(
        title=_("Rollover button"),
        required=False,
    )
    
