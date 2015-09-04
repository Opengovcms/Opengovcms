from zope.component import queryUtility, getMultiAdapter
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry

from interfaces import ISocialShareSettings

class SocialshareIcons(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def get_icons(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ISocialShareSettings, check=False)
        #Only visible items
        items = settings.social_share_items or []
        icons = [item for item in items if item.visible]
        #Sort on priority
        icons.sort(key=lambda x: x.priority)
        
        dropdown = settings.style == 2
        button_1 = settings.button_1 and settings.button_1.decode() or None
        button_2 = settings.button_2 and settings.button_2.decode() or None

        danish = self.is_danish()
        icns = []
        for icon in icons:
            icns.append({'icon_1': icon.icon_1 and icon.icon_1.encode() or None,
                         'icon_2': icon.icon_1 and icon.icon_2.encode() or None,
                         'alt': danish and icon.dk_alt or icon.uk_alt,
                         'url': icon.url
                        })

        return {'icons':icns, 
                'dropdown': dropdown,
                'button_1': button_1,
                'button_2': button_2}

    def is_danish(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        current_language = portal_state.language()
        return current_language == 'da'
