from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from policy.content.gallery_page import IBottomText

from collective.plonetruegallery.browser.views.galleryview import GalleryView
from collective.plonetruegallery.utils import getGalleryAdapter
from collective.plonetruegallery.settings import GallerySettings
from zope.component import getMultiAdapter

class GalleryPageView(GalleryView):

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def bottom_text(self):
        pass

class GalleryFolderView(GalleryView):

    def __init__(self, context, request):
        super(GalleryView, self).__init__(context, request)
