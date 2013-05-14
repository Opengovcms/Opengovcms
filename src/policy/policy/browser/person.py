# -*- coding: utf-8 -*-
from Acquisition import aq_inner
import vobject

from Products.Five.browser import BrowserView

class PersonView(BrowserView):
    """ """ 
    def generate_vcard(self):
        """Generates af VCard """
        context = aq_inner(self.context)

        # XXX department type not implemented yet
        # XXX vcard download from vtu.addressbook.types not yet tested.
        department = None
        if len(context.departments) > 0:
            department = context.departments[0].to_object
        
        card = vobject.vCard()
        card.add('fn').value = context.title
        card.add('n').value = vobject.vcard.Name(given=context.firstname,
                                                 family=context.lastname,)
        card.add('org').value = [getattr(department, 'title', u''),]
        card.add('adr').value = vobject.vcard.Address(
                street=getattr(department, 'street', u''),
                city=getattr(department, 'city', u''),
                country=u'Denmark',
                code=getattr(department, 'zipcode', u''),)
                          
        card.adr.type_param = [u'WORK']
        card.add('title').value = context.jobtitle
        card.add('email').value = context.email
        card.email.type_param = [u'INTERNET', u'WORK']
        card.add('tel').value = context.phone
        card.tel.type_param = [u'WORK']
        return card.serialize()

    def download_vcard(self):
        """downloads vcard"""
        vcard = self.generate_vcard()
        filename = self.context.getId()
        self.request.response.setHeader('Content-type', 'text/x-vcard')
        self.request.response.setHeader('Content-encoding', 'utf-8')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename=%s.vcf' % filename)
        if isinstance(vcard, unicode):
            return vcard.encode('utf-8')
        return vcard
