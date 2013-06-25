from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from plone.app.contenttypes.migration import migration

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
