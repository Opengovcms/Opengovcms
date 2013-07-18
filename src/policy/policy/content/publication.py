# -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from plone.dexterity.content import Item

class IPublication(Interface):
    """ Publication """

class Publication(Item):
    implements(IPublication)
