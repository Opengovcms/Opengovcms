# -*- coding: utf-8 -*-
from plone.directives import form
from plone.app.textfield import RichText
from collective import dexteritytextindexer

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
