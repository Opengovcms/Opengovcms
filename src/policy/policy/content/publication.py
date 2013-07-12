# -*- coding: utf-8 -*-
from zope import schema

from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.directives import form
from plone.app.textfield import RichText
from collective import dexteritytextindexer

from policy import validators
from policy.i18n import MessageFactory as _
from Products.CMFPlone import PloneMessageFactory as _pmf
from plone.app.imagecropping.interfaces import IImageCropping


class IPublication(form.Schema, IImageCropping):
    """ Publication """

    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_pmf(u"Text"),
        description=_(u""),
        required=False,
    )
