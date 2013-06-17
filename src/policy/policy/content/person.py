# -*- coding: utf-8 -*-
from zope import schema
from plone.directives import form

from plone.dexterity.content import Item

from collective import dexteritytextindexer

from plone.app.textfield import RichText

from plone.namedfile.field import NamedBlobImage

from Products.CMFPlone import PloneMessageFactory as _pmf
from policy.i18n import MessageFactory as _

from plone.app.imagecropping.interfaces import IImageCropping


class IMinimalPerson(form.Schema):
    """ Minimal """

    dexteritytextindexer.searchable('firstname')
    firstname = schema.TextLine(
        title=_(u"First name"),
        required=True,
    )

    dexteritytextindexer.searchable('lastname')
    lastname = schema.TextLine(
        title=_(u"Last name"),
        required=True,
    )


class IPerson(IMinimalPerson, IImageCropping):
    """ Represents an Person.
        Displayed in a contacts portlet.
        """

    dexteritytextindexer.searchable('initials')
    initials = schema.TextLine(
        title=_(u"Initials"),
        required=False,
    )

    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_(u"Email"),
        required=False,
    )

    dexteritytextindexer.searchable('phone')
    phone = schema.TextLine(
        title=_(u"Phone"),
        required=False,
    )

    dexteritytextindexer.searchable('jobtitle')
    jobtitle = schema.TextLine(
        title=_(u"Danish Job title"),
        required=False,
    )

    # Seems to be fivu stuff?
    # dexteritytextindexer.searchable('english_jobtitle')
    # english_jobtitle = schema.TextLine(
    #     title=_(u"English Job title"),
    #     required=False,
    # )

    # dexteritytextindexer.searchable('functiontitle')
    # functiontitle = schema.TextLine(
    #     title=_(u"Danish Function title"),
    #     required=False,
    # )

    # dexteritytextindexer.searchable('english_functiontitle')
    # english_functiontitle = schema.TextLine(
    #     title=_(u"English Function title"),
    #     required=False,
    # )

    qrcodeurl = schema.URI(
        title=_(u"QR code URL"),
        required=False,
    )

    image = NamedBlobImage(
        title=_(u"Portrait"),
        description=_(u"A portrait of this person. "
                      u"This should be in standard portrait orientation."),
        required=False
    )

    hideimage = schema.Bool(
        title=u'Hide image',
        required=False,
    )

    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_(u"Text"),
        required=False,
    )


class Person(Item):
    """Customised Expert content class"""

    @property
    def title(self):
        names = [
            self.firstname,
            self.lastname,
        ]
        return u' '.join([name for name in names if name])

    def setTitle(self, value):
        return
