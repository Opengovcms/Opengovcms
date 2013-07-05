from Products.CMFQuickInstallerTool.interfaces import INonInstallable
from plone.app.contenttypes.migration import migration
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implements


class HiddenProducts(object):
    implements(INonInstallable)

    def getNonInstallableProducts(self):
        return [
            'PloneFormGen',
            'Products.PloneFormGen',
            'Products.windowZ',
            'collective.js.jqueryui',
            'collective.panels',
            'collective.portlet.carousel',
            'collective.portlet.ngcollection',
            'collective.portlet.rich',
            'collective.portletmetadata',
            'collective.z3cform.datetimewidget',
            'plone.app.caching',
            'plone.app.collection',
            'plone.app.contenttypes',
            'plone.app.dexterity',
            'plone.app.imagecropping',
            'plone.app.intid',
            'plone.app.jquery',
            'plone.app.jquerytools',
            'plone.app.relationfield',
            'plone.app.theming',
            'plone.formwidget.autocomplete',
            'plone.formwidget.contenttree',
            'plone.formwidget.querystring',
            'plone.resource',
            'plonetheme.classic',
            'quintagroup.plonetabs',
            'quintagroup.portlet.generichtml',
            'smtemplate.theme',
            'windowZ',
            ]

    def getNonInstallableProfiles(self):
        return [
            'Products.PloneFormGen:default',
            'Products.windowZ:default',
            'collective.js.jqueryui:default',
            'collective.panels:default',
            'collective.portlet.carousel:default',
            'collective.portlet.ngcollection:default',
            'collective.portlet.rich:default',
            'collective.portletmetadata:default',
            'collective.z3cform.datetimewidget:default',
            'plone.app.caching:default',
            'plone.app.collection:default',
            'plone.app.contenttypes:default',
            'plone.app.dexterity:default',
            'plone.app.imagecropping:default',
            'plone.app.intid:default',
            'plone.app.jquery:default',
            'plone.app.jquerytools:default',
            'plone.app.relationfield:default',
            'plone.app.theming:default',
            'plone.formwidget.autocomplete:default',
            'plone.formwidget.contenttree:default',
            'plone.formwidget.querystring:default',
            'plone.resource:default',
            'plonetheme.classic:default',
            'quintagroup.plonetabs:default',
            'quintagroup.portlet.generichtml:default',
            'smtemplate.theme:default',
            ]

def migrateAT2DX(context):
    """
    @param context: Products.GenericSetup.context.DirectoryImportContext instance
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('migrateAT2DX.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()
    migration.migrate_folders(portal)
    migration.migrate_documents(portal)
    migration.migrate_collections(portal)
    migration.migrate_blobimages(portal)
    migration.migrate_blobfiles(portal)
    migration.migrate_blobnewsitems(portal)
    migration.restoreReferences(portal)
    migration.restoreReferencesOrder(portal)
