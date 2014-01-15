# Patch broken sortable_title indexer
# We're simply using the old plone 3 implementation
# New plone 4 version calls mapUnicode which doesn't work with danish chars

from Products.CMFPlone.CatalogTool import num_sort_regex, zero_fill
from Products.CMFPlone.utils import safe_callable
from Products.CMFPlone.utils import safe_unicode
from plone.indexer import indexer
from Products.CMFCore.interfaces import IContentish
import locale

@indexer(IContentish)
def sortable_title(obj):
    """ Helper method for to provide FieldIndex for Title.

    >>> from Products.CMFPlone.CatalogTool import sortable_title

    >>> self.folder.setTitle('Plone42 _foo')
    >>> sortable_title(self.folder, self.portal)
    'plone000042 _foo'
    """
    title = getattr(obj, 'Title', None)
    if title is not None:
        if safe_callable(title):
            title = title()

        if isinstance(title, basestring):
            # Ignore case, normalize accents, strip spaces
            sortabletitle = safe_unicode(title).lower().strip()
            # Replace numbers with zero filled numbers
            sortabletitle = num_sort_regex.sub(zero_fill, sortabletitle)
            # Truncate to prevent bloat
            sortabletitle = sortabletitle[:70].encode('utf-8')
            return locale.strxfrm(sortabletitle)

    return ''
