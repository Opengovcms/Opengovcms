# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.indexer.decorator import indexer

from person import IPerson
from categorization import ISMCategorization

from plone.i18n.normalizer.interfaces import INormalizer

@indexer(IPerson)
def lastname(person):
    return getUtility(INormalizer).normalize(person.lastname)

@indexer(ISMCategorization)
def subject_values_indexer(context):
    return context.subject_values

@indexer(ISMCategorization)
def section_indexer(context):
    return context.section

@indexer(ISMCategorization)
def suppl_category_indexer(context):
    return context.suppl_category
