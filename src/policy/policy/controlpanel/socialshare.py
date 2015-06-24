from Products.CMFCore.interfaces import ISiteRoot
from plone.z3cform import layout

from zope.component import queryUtility, adapter
from plone.registry.interfaces import IRegistry

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from interfaces import ISocialShareSettings, ISocialShareItem

img_tmpl = ViewPageTemplateFile("templates/image_widget.pt")
multi_widget_field_tpl = ViewPageTemplateFile("templates/multi_widget_field.pt")
multi_widget_tpl = ViewPageTemplateFile("templates/multi_widget.pt")
configlet_tpl = ViewPageTemplateFile('templates/configlet.pt')

class SocialShareSettingsEditForm(RegistryEditForm):
    """Social share settings form"""

    schema = ISocialShareSettings
    label = u"Social share settings"

    def get_settings(self):
        registry = queryUtility(IRegistry)
        return registry.forInterface(ISocialShareSettings, check=False)

    def updateFields(self):
        super(SocialShareSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(SocialShareSettingsEditForm, self).updateWidgets()
        settings = self.get_settings()
        
        self.widgets["button_1"].template = img_tmpl
        self.widgets["button_2"].template = img_tmpl

        self.widgets["button_1"].icon_data = settings.button_1 and settings.button_1.decode() or ''
        self.widgets["button_2"].icon_data = settings.button_2 and settings.button_2.decode() or ''
        
        self.widgets['social_share_items'].template = multi_widget_tpl

        for idx, widget in enumerate(self.widgets['social_share_items'].widgets):
            widget.template = multi_widget_field_tpl
            widget.subform.widgets['icon_1'].template = img_tmpl
            widget.subform.widgets['icon_2'].template = img_tmpl
            if idx < len(settings.social_share_items or []):
                widget.subform.widgets['icon_1'].icon_data = settings.social_share_items[idx].icon_1 and settings.social_share_items[idx].icon_1.decode() or ''
                widget.subform.widgets['icon_2'].icon_data = settings.social_share_items[idx].icon_2 and settings.social_share_items[idx].icon_2.decode() or ''

    def extractData(self):
        """overrided to prevent missing old value of images 
        if fields are left empty
        """

        data, errors = super(SocialShareSettingsEditForm, self).extractData()
        if errors:
            return data, errors

        settings = self.get_settings()

        if settings.button_1 and not data['button_1']:
            data['button_1'] = settings.button_1

        if settings.button_2 and not data['button_2']:
            data['button_2'] = settings.button_2

        items = settings.social_share_items
        items_count = len(settings.social_share_items or []) 
        if items:
            for idx, item in enumerate(data['social_share_items']):
                obj =  idx < items_count and items[idx] or []
                if not obj:
                    continue
                item_icon_1 = obj.icon_1 or None
                item_icon_2 = obj.icon_2 or None
                try:
                    if item_icon_1 and not item.icon_1:
                        data['social_share_items'][idx].icon_1 = item_icon_1 
                
                    if item_icon_2 and not item.icon_2:
                        data['social_share_items'][idx].icon_2 = item_icon_2
                except IndexError:
                    pass
        data = self._extract_image_urls(data)
        return data, errors

    def _extract_image_urls(self, data):
        url = 'data:%s;base64,%s' 

        bt1_ctype = self.request.get('form.widgets.button_1').headers['Content-Type']
        bt2_ctype = self.request.get('form.widgets.button_2').headers['Content-Type']

        if bt1_ctype.startswith('image'):
            data['button_1'] = url % (bt1_ctype, data['button_1'].encode('base64').encode())

        if bt2_ctype.startswith('image'):
            data['button_2'] = url % (bt2_ctype, data['button_2'].encode('base64').encode())

        for idx, item in enumerate(data['social_share_items']):
            icn1_ctype = self.request.get('form.widgets.social_share_items.%d.widgets.icon_1' % idx).headers['Content-Type']
            icn2_ctype = self.request.get('form.widgets.social_share_items.%d.widgets.icon_2' % idx).headers['Content-Type']

            if icn1_ctype.startswith('image'):
                data['social_share_items'][idx].icon_1 = url % (icn1_ctype, data['social_share_items'][idx].icon_1.encode('base64').encode())

            if icn2_ctype.startswith('image'):
                data['social_share_items'][idx].icon_2 = url % (icn2_ctype, data['social_share_items'][idx].icon_2.encode('base64').encode())

        return data

class SocialShareSettingsControlPanel(layout.FormWrapper):
    form = SocialShareSettingsEditForm
    index = configlet_tpl

