import zope.component
from zope.schema.vocabulary import SimpleTerm
from zope.pagetemplate.interfaces import IPageTemplate
from z3c.form.widget import SequenceWidget
from z3c.form.browser.radio import RadioWidget

def renderForValue(self, value):
    terms = list(self.terms)
    try:
        term = self.terms.getTermByToken(value)
    except LookupError:
        if value == SequenceWidget.noValueToken:
            term = SimpleTerm(value)
            terms.insert(0, term)
        else:
             raise

    checked = self.isChecked(term)
    id = '%s-%i' % (self.id, terms.index(term))
    item = {'id': id, 'name': self.name, 'value': term.token,
            'checked': checked}
    template = zope.component.getMultiAdapter(
        (self.context, self.request, self.form, self.field, self),
        IPageTemplate, name=self.mode + '_single')
    return template(self, item)

RadioWidget.renderForValue = renderForValue
