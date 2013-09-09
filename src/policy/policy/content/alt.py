from z3c.form.interfaces import IEditForm, IAddForm
from zope.interface import alsoProvides
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.supermodel import model
from policy.i18n import MessageFactory as _


class IAltImageText(model.Schema):
    """Behavior interface to set alt image text for content with image fields
    """

    alt_image_text = schema.TextLine(
        title=_(
            u'label_alt_image_text',
            default=u'Alt image text'
        ),
        description=_(
            u'help_alt_image_text',
            default=u'Alt text for image'
        ),
        required=False
    )

    form.omitted('alt_image_text')
    form.no_omit(IEditForm, 'alt_image_text')
    form.no_omit(IAddForm, 'alt_image_text')

alsoProvides(IAltImageText, IFormFieldProvider)
