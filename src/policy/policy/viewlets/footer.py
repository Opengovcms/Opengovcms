# -*- coding: utf-8 -*-

from policy.interfaces import ISiteSettings

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry

from zope.component import ComponentLookupError
from zope.component import getUtility


class FooterViewlet(ViewletBase):
    index = ViewPageTemplateFile('footer.pt')

    @property
    def contents(self):
        try:
            settings = getUtility(IRegistry).forInterface(ISiteSettings)
        except KeyError:
            raise ComponentLookupError(ISiteSettings)

        return settings.address
