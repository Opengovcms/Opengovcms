# -*- coding: utf-8 -*-
import time
import csv
import StringIO

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from plone.app.textfield.interfaces import IRichTextValue

from zope.component import getMultiAdapter

from policy.i18n import MessageFactory as _


class PublicationView(BrowserView):
    """ """

    @property
    def has_image(self):
        return self.context.publication_cover_image is not None

    @property
    def image_url(self):
        scale = getMultiAdapter(
            (self.context, self.context.REQUEST),
            name='images'
        )
        url = scale.scale('publication_cover_image', scale='mini').url
        return url

    @property
    def image_caption(self):
        if hasattr(self.context, 'publication_cover_caption') and \
                getattr(self.context, 'publication_cover_caption'):
            return getattr(self.context, 'publication_cover_caption')
        return _(u'Cover image text is missing')

    def related_items(self):
        '''Returns list of related items.
        '''

        context = self.context

        return context.Schema()['relatedItems'].get(context)

class CSVExportView(BrowserView):

    def get_data(self, export_fields, limit=10000):
        """ """
        cat = getToolByName(self.context, 'portal_catalog')
        offset = self.request.get('offset', None)
        query = {'portal_type': 'Publication'}

        if offset:
            dt = DateTime(offset)
            query['Date'] = {"query": DateTime(dt), "range": "min"}

        brains = cat.searchResults(**query)

        res = []
        for brain in brains[:limit]:
            line = {}
            obj = brain.getObject()
            line['url'] = obj.absolute_url()

            for field_id in export_fields:
                v = getattr(obj, field_id, None)
                if IRichTextValue.providedBy(v):
                    v = v.output
                line[field_id] = v
            res.append(line)

        return res

    def generate_csv(self, fields, rows):
        f = StringIO.StringIO()
        writer = csv.DictWriter(f, fields)
        headers = dict((n, n) for n in fields)
        writer.writerow(headers)

        writer.writerows(rows)
        output = f.getvalue()
        f.close()
        return output

    def __call__(self):
        """ """
        export_fields = ('title', 'description', 'text', 'author', 'publisher',
                         'version', 'publication_year', 'pagecount', 'isbn', 
                         'iisbn', 'issn', 'iissn', 'issuu_url')

        csv_fields = ('url',) + export_fields
        data = self.get_data(export_fields)
        csvfile = self.generate_csv(csv_fields, data)

        filename = "publications-%s.csv" % time.strftime("%Y%m%d-%H%M%S", time.localtime())

        self.request.response.setHeader('Content-Type', 'text/csv; charset=utf-8')
        self.request.response.setHeader('Content-Length', len(csvfile))
        self.request.response.setHeader('Content-Disposition', 
                                        'attachment; filename="%s"' % filename)

        return csvfile
