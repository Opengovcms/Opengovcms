from policy.i18n import MessageFactory as _
from policy.interfaces import ISiteSettings
from zope.interface import Interface
from zope import schema

from plone.app.registry.browser import controlpanel
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.z3cform import layout

from z3c.form import field


class ControlPanelEditForm(controlpanel.RegistryEditForm):
    schema = ISiteSettings
    fields = field.Fields(ISiteSettings)
    fields['address'].widgetFactory = WysiwygFieldWidget

    label = _(u"Configure site")
    description = _(
        u"This form lets you configure the site specific settings."
    )


ControlPanel = layout.wrap_form(
    ControlPanelEditForm,
    controlpanel.ControlPanelFormWrapper
)


class IFlyoutSettings(Interface):
    """ Fly out menu settings """


class FlyoutControlPanelEditForm(controlpanel.RegistryEditForm):
    schema = IFlyoutSettings
    fields = field.Fields(IFlyoutSettings)

    label = _(u"Configure fly-out menu")
    description = _(
        u"Here you can edit the content of the fly-out menu."
    )


FlyoutControlPanel = layout.wrap_form(
    FlyoutControlPanelEditForm,
    controlpanel.ControlPanelFormWrapper
)
# todo: set index
