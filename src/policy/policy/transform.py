from plone.transformchain.interfaces import ITransform

from zope.interface import implements, Interface
from zope.component import adapts

from lxml.html import HtmlElement


class FixLinefeedTransform(object):
    """
       This adapter is implemented to avoid &#10; and &#13; in transformed
       output.

       The problem should be fixed in Plone
    """

    implements(ITransform)
    adapts(Interface, Interface)

    order = 10000

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def transformString(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformUnicode(self, result, encoding):
        return self.transformIterable([result], encoding)

    def recurse(self, tree):
        # We will only handle elements from lxml.html, I am not sure if
        # the other functions are ever invoked.

        if type(tree) != HtmlElement:
            return

        children = None
        try:
            children = tree.getchildren()
        except:
            # reached leaf node
            pass

        for i in tree.keys():
            node_value = tree.get(i)
            if '\n' in node_value or '\r' in node_value:
                new_value = node_value.replace('\r', '')
                new_value = new_value.replace('\n', '')
                tree.set(i, new_value)

        if children:
            for node in children:
                self.recurse(node)

    def transformIterable(self, result, encoding):
        if hasattr(result, 'tree'):
            root = result.tree.getroot()
            self.recurse(root)

            result = str(result).replace('&#13;&#10;', '\n')
        return result
