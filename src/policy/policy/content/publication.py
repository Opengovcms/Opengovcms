# -*- coding: utf-8 -*-
from zope import schema

from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.directives import form
from plone.app.textfield import RichText
from collective import dexteritytextindexer

from policy import validators
from policy.i18n import MessageFactory as _
from Products.CMFPlone import PloneMessageFactory as _pmf

class IPublication(form.Schema):
    """ Publication """

    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_pmf(u"Text"),
        description=_(u""),
        required=False,
    )

    publication_cover_image = NamedBlobImage(
        title=_(u"Cover image"),
        description=_(u"Upload the cover of the publication."),
        required=False
        )

    publication_cover_caption = schema.TextLine(
        title=_(u'label_publication_cover_caption', default=u"Cover caption"),
        description=_(u"help_publication_cover_caption",
                      default=u"Caption for the cover image."),
        required=False
        )

    files = NamedBlobFile(
        title=_(u"Publication file"),
        description=_('Upload the publication file, e.g. a PDF file.'),
        required=False,
        )

    author = schema.TextLine(
        title=_(u"Publication author"),
        description=_(u"Name of the publication author, e.g. John Doe."),
        required=False
        )
    
    publisher = schema.TextLine(
        title=_(u"Publication publisher"),
        description=_(u"Institution behind the publication."),
        required=False
        )

    version = schema.TextLine(
        title=_(u"Version"),
        description=_(u"Enter version"),
        required=False
        )

    pagecount = schema.Int(
        title=_(u"Page count"),
        description=_(u"Number of pages of the publication."),
        required=False,
        )

    isbn = schema.TextLine(
        title=_(u'label_isbn', default=u'ISBN'),
        description=_(u"help_isbn",
                      default=u"The ISBN record identifier for this publication."),
        required=False,
        constraint=validators.stdnum_validator('isbn'),
        )

    iisbn = schema.TextLine(
        title=_(u'label_internet_isbn', default=u'Internet ISBN'),
        description=_(u"help_internet_isbn",
                      default=u"The Internet ISBN record identifier for this publication."),
        required=False,
        constraint=validators.stdnum_validator('isbn'),
        )

    issn = schema.TextLine(
        title=_(u'label_issn', default=u'ISSN'),
        description=_(u"help_issn",
                      default=u"The ISSN record identifier for this publication."),
        required=False,
        constraint=validators.stdnum_validator('issn'),
        )

    iissn = schema.TextLine(
        title=_(u'label_internet_issn', default=u'Internet ISSN'),
        description=_(u"help_internet_issn",
                      default=u"The Internet ISSN record identifier for this publication."),
        required=False,
        constraint=validators.stdnum_validator('issn'),
        )


    publication_year = schema.Int(
        title=_(u'label_publication_year', default=u"Year of publication"),
        description=_(u"help_publication_year",
                      default=u"The year this publication was first published."),
        required=False
        )

    issuu_url = schema.Int(
        title=_(u"Issuu URL"),
        description=_(u"Add a link to Issuu version of the publication, e.g http://www.issuu.com/myaccount/docs/mypublication."),
        required=False
        )


    

