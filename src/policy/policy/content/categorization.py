# -*- coding: utf-8 -*-
from z3c.form.interfaces import IEditForm, IAddForm
from zope.interface import alsoProvides
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.supermodel import model
from plone.app.dexterity import MessageFactory as _


class ISMCategorization(model.Schema):
    """Behavior interface with three categorization options.
    """

    model.fieldset(
        'categorization',
        label=_(u"Categorization"),
        fields=['subject_values', 'section', 'suppl_category']
    )

    subject_values = schema.List(
            value_type=schema.Choice(
                title=u"Emneord",
                vocabulary="smtemplate.SubjectVocabulary"),
            title=u"Emneord",
            description=u"Vælg et eller flere emneord."
        )
    section = schema.Choice(
            title=u"Sektion",
            vocabulary="smtemplate.SectionVocabulary",
            required=False
        )
    suppl_category = schema.List(
            value_type=schema.Choice(
                vocabulary="smtemplate.SupplCategoryVocabulary"),
            title=u"Supplerende kategorisering",
            description=u"Vælg en eller flere værdier."
        )

    # Only show on add/edit forms
    form.omitted('subject_values')
    form.no_omit(IEditForm, 'subject_values')
    form.no_omit(IAddForm, 'subject_values')
    form.omitted('section')
    form.no_omit(IEditForm, 'section')
    form.no_omit(IAddForm, 'section')
    form.omitted('suppl_category')
    form.no_omit(IEditForm, 'suppl_category')
    form.no_omit(IAddForm, 'suppl_category')

alsoProvides(ISMCategorization, IFormFieldProvider)
