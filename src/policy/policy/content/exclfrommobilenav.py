from z3c.form.interfaces import IEditForm, IAddForm
from zope.interface import alsoProvides
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.supermodel import model
from plone.app.dexterity import MessageFactory as _


class IExcludeFromMobileNavigation(model.Schema):
    """Behavior interface to exclude items from mobile navigation.
       A copy of p.a.dexterity IExcludeFromNavigation
    """

    model.fieldset(
        'settings',
        label=_(u"Settings"),
        fields=['exclude_from_mobile_nav']
    )

    exclude_from_mobile_nav = schema.Bool(
        title=_(
            u'label_exclude_from_mobile_nav',
            default=u'Exclude from mobile navigation'
        ),
        description=_(
            u'help_exclude_from_mobile_nav',
            default=u'If selected, this item will not appear in the ' +
                    u'navigation tree on small screens'
        ),
        default=False
    )

    form.omitted('exclude_from_mobile_nav')
    form.no_omit(IEditForm, 'exclude_from_mobile_nav')
    form.no_omit(IAddForm, 'exclude_from_mobile_nav')

alsoProvides(IExcludeFromMobileNavigation, IFormFieldProvider)
