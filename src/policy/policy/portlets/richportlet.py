# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.rich import RichPortletMessageFactory as _
from plone.app.portlets.browser import z3cformhelper
from plone.app.portlets.portlets import base
from plone.app.textfield import RichText
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.portlets.interfaces import IPortletDataProvider
from z3c.form import field
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.component import getUtility, getMultiAdapter
from zope.interface import implements

from collective.portlet.rich.richportlet import background_placement


class IRichPortlet(IPortletDataProvider):
    """A portlet which renders predefined static HTML.

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    target_title_image = RelationChoice(
        title=_(u"Portlet title image"),
        description=_(u"Find the image"),
        required=False,
        source=ObjPathSourceBinder(
            portal_type=['Image']
        ),
    )

    image_alt_text = schema.TextLine(
        title=u"Image alt tekst",
        required=False
    )

    title_image_scale = schema.Choice(
        title=_(u"Portlet title image scale"),
        description=_(u"Choose the image scale."),
        required=False,
        vocabulary='collective.portlet.rich.vocabularies.ImageScalesVocabulary',
    )

    title_image_background = schema.Bool(
        title=_(u"Title image is background?"),
        required=False
    )

    title_image_background_placement = schema.Choice(
        title=_(u"Background placement"),
        required=False,
        vocabulary=background_placement
    )

    title = schema.TextLine(
        title=_(u"Portlet title"),
        description=u"Titel. Hvis title ikke skal vises, vælges 'Vis ikke portletkant'.",
        required=True
    )

    title_more_url = schema.ASCIILine(
        title=_(u"Portlet title details link"),
        description=_(u"If given, the title "
                      "will link to this URL."),
        required=False
    )

    text = RichText(
        title=_(u"Text"),
        description=_(u"The portlet body text."),
        required=False
    )

    omit_border = schema.Bool(
        title=_(u"Omit portlet border"),
        description=_(u"Tick this box if you want to render the text above without the "
                      "standard header, border or footer."),
        required=True,
        default=False
    )

    footer = schema.TextLine(
        title=_(u"Portlet footer"),
        description=_(u"Text to be shown in the footer"),
        required=False
    )

    footer_more_url = schema.ASCIILine(
        title=_(u"Portlet footer details link"),
        description=_(u"If given, the footer will link to this URL."),
        required=False
    )


IRichPortlet.setTaggedValue(
    u'plone.formwidget.contenttree.startuppath', 'context'
)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IRichPortlet)

    # backwards compatibility
    title_image_scale = ''
    title_image_background = False
    title_image_background_placement = None
    target_title_image = None
    title_more_url = None
    title = u"Rich portlet"
    image_alt_text = None


    def __init__(
        self, target_title_image=None, title_image_background=False,
        title_image_scale='',
        title_image_background_placement=None, title=u"",
        title_more_url='', text=u"",
        omit_border=False,
        footer=u"", footer_more_url='',
        header=None, target_header_image=None, header_more_url=None,
        image_alt_text=None
    ):
        """Initialize all variables."""

        self.target_title_image = target_title_image
        self.title_image_scale = ''
        self.title_image_background = title_image_background
        self.title_image_background_placement = title_image_background_placement
        self.title = title or Assignment.title
        self.title_more_url = title_more_url
        self.text = text
        self.omit_border = omit_border
        self.footer = footer
        self.footer_more_url = footer_more_url
        self.image_alt_text = image_alt_text

        # backwards compatibility
        if header is not None:
            self.title = header

        if target_header_image is not None:
            self.target_title_image = target_header_image

        if header_more_url is not None:
            self.title_more_url = header_more_url


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('richportlet.pt')

    #also taken from collection portlet
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.portal = portal_state.portal()

    def css_class(self):
        """Generate a CSS class from the portlet title
        """
        title = self.data.title
        normalizer = getUtility(IIDNormalizer)
        return "portlet-richportlet-%s" % normalizer.normalize(title)

    def has_title_link(self):
        return bool(self.data.title_more_url)

    def has_text(self):
        return bool(self.data.text)

    def has_footer_link(self):
        return bool(self.data.footer_more_url)

    def has_footer(self):
        return bool(self.data.footer)

    def has_title_image(self):
        return bool(self.data.target_title_image)

    def image_is_background(self):
        return bool(self.data.title_image_background)

    def get_text(self):
        return self.data.text

    def get_placement(self):
        return self.data.title_image_background_placement

    def get_title_image_tag(self):
        """Generate image tag.

        Note: ``target_title_image`` uses the uberselection-widget
        and does not return an object (unlike Archetypes reference
        fields).
        """

        if self.image_is_background():
            return None

        ref = self.data.target_title_image
        if ref is None:
            return

        image = ref.to_object

        if IImageScaleTraversable and IImageScaleTraversable.providedBy(image):
            try:
                view = image.restrictedTraverse('@@images')
                view = view.__of__(image)
                return view.tag('image', scale=self.data.title_image_scale,
                                alt=self.data.image_alt_text)
            except:
                pass

    def get_background_image_url(self):
        ref = self.data.target_title_image
        if ref is None:
            return

        image = ref.to_object

        if IImageScaleTraversable and IImageScaleTraversable.providedBy(image):
            try:
                view = image.restrictedTraverse('@@images')
                view = view.__of__(image)
                return view.scale('image', scale=self.data.title_image_scale).url
            except:
                return ''

    def get_div_style(self):
        result = {}
        if self.image_is_background():
            result['background'] = "url('" + self.get_background_image_url() + "') no-repeat"

        return '; '.join([k + ': ' + v for (k, v) in result.items()])


class AddForm(z3cformhelper.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    label = _(u"Add Rich Portlet")
    description = _(u"This portlet ...")

    fields = field.Fields(IRichPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    label = _(u"Edit Rich Portlet")
    description = _(u"This portlet ...")

    fields = field.Fields(IRichPortlet)
