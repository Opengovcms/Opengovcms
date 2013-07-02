from policy.i18n import MessageFactory as _
from policy.interfaces import ISiteSettings
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope import schema
from Acquisition import aq_inner

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.registry.browser import controlpanel
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.z3cform import layout
from plone.z3cform.layout import FormWrapper

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
    # so far no settings here.


class FlyoutControlPanelEditForm(controlpanel.RegistryEditForm):
    schema = IFlyoutSettings
    fields = field.Fields(IFlyoutSettings)

    label = _(u"Configure fly-out menu")
    description = _(
        u"Here you can edit the content of the fly-out menu."
    )


class FlyoutControlPanel(FormWrapper):

    form = FlyoutControlPanelEditForm
    index = ViewPageTemplateFile('templates/controlpanel_flyout.pt')

    def top_menu_items(self):
        context = aq_inner(self.context)
        portal_tabs_view = getMultiAdapter((context, self.request),
                                           name='portal_tabs_view')
        return portal_tabs_view.topLevelTabs()
