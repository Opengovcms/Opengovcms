from plone.app.search.browser import Search as SearchBase
from Products.CMFCore.utils import getToolByName

class Search(SearchBase):

    def filter_types(self, types):
        return ['Document', 'Event', 'News Item']