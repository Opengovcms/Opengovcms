# -*- encoding: utf-8 -*-
from zope import interface
from zope.schema import interfaces
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot

from Products.ATVocabularyManager import NamedVocabulary

def get_atvm_terms(name):
    portal = getUtility(ISiteRoot)
    try:
        items = NamedVocabulary(name).getVocabularyDict(portal).items()
    except KeyError:
        items = []
    return [SimpleTerm(value, value, title.decode('utf-8')) for value, title in items]


def subject_values(context):
    return SimpleVocabulary(
                get_atvm_terms("emneord")
           )
interface.alsoProvides(subject_values, interfaces.IVocabularyFactory)

def section(context):
    return SimpleVocabulary(
                get_atvm_terms("sektioner")
           )
interface.alsoProvides(section, interfaces.IVocabularyFactory)

def supplcategory(context):
    return SimpleVocabulary(
                get_atvm_terms("supplcategory")
           )
interface.alsoProvides(supplcategory, interfaces.IVocabularyFactory)
