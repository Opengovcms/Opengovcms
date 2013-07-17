# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.indexer.decorator import indexer

from person import IPerson

from plone.i18n.normalizer.interfaces import INormalizer

@indexer(IPerson)
def lastname(person):
    return getUtility(INormalizer).normalize(person.lastname)

