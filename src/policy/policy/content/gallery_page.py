# -*- coding: utf-8 -*-

from zope.interface import Interface, implements
from plone.dexterity.content import Item

from zope.interface import alsoProvides, Interface
from z3c.relationfield.schema import Relation, RelationChoice
from plone.supermodel.model import Fieldset
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.textfield import RichText as RichTextField
from zope.component import adapts
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.dexterity.interfaces import IDexterityContent

from policy.i18n import MessageFactory as _


class IRelatedGallery(Interface):
    """Behavior interface to make a Dexterity type support related items.
    """
    gallery = RelationChoice(
        title=u'Related Gallery',
        default=None,
        source=ObjPathSourceBinder(portal_type=['Folder']),
        required=False,
    )
alsoProvides(IRelatedGallery, IFormFieldProvider)

class IBottomText(Interface):
    """Bottom text behavior
    """
    bottom_text = RichTextField(
        title=u'Bottom Text',
        description=u"",
        required=False,
    )
alsoProvides(IBottomText, IFormFieldProvider)


class RelatedGallery(object):
    implements(IRelatedGallery)
    adapts(IDexterityContent)

class BottomText(object):
    implements(IBottomText)
    adapts(IDexterityContent)


class IGalleryPage(Interface):
    """ IGalleryPage """


class GalleryPage(Item):
    implements(IGalleryPage)
