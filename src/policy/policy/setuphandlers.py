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
            'plone.app.dexterity',
            'plone.formwidget.autocomplete',
            'plone.formwidget.contenttree',
            'plone.app.contenttypes',
            'plone.app.theming',
            'plone.app.caching',
            'plone.app.imagecropping',
            'plone.app.relationfield',
            'collective.z3cform.datetimewidget',
            'collective.panels',
            'windowZ',
            'Products.windowZ',
            'collective.portlet.rich',
            'quintagroup.portlet.generichtml',
            'collective.portlet.ngcollection',
            'collective.portlet.carousel',
            'collective.portletmetadata',
            'smtemplate.theme',
            ]

    def getNonInstallableProfiles(self):
        return [
            'Products.PloneFormGen:default',
            'plone.app.dexterity:default',
            'plone.formwidget.autocomplete',
            'plone.formwidget.contenttree',
            'plone.app.contenttypes:default',
            'plone.app.theming:default',
            'plone.app.caching:default',
            'plone.app.imagecropping:default',
            'plone.app.relationfield:default',
            'collective.z3cform.datetimewidget:default',
            'collective.panels:default',
            'Products.windowZ:default',
            'collective.portlet.rich:default',
            'quintagroup.portlet.generichtml:default',
            'collective.portlet.ngcollection:default',
            'collective.portlet.carousel:default',
            'collective.portletmetadata:default',
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
