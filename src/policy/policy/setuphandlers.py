from Products.CMFQuickInstallerTool.interfaces import INonInstallable
from plone.app.contenttypes.migration import migration
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

class HiddenProducts(object):
    implements(INonInstallable)

    def getNonInstallableProducts(self):
        return [
            'PloneFormGen',
            'Products.PloneFormGen',
            'ATVocabularyManager',
            'Products.ATVocabularyManager',
            'Products.windowZ',
            'collective.chimpfeed',
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
            'plone.app.versioningbehavior',
            ]

    def getNonInstallableProfiles(self):
        return [
            'Products.PloneFormGen:default',
            'Products.ATVocabularyManager:default',
            'Products.windowZ:default',
            'collective.chimpfeed:default',
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
            'plone.app.versioningbehavior:default'
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


catalog_indexes = (
    {'name': 'lastname',
     'type': 'FieldIndex', },
    {'name': 'smtemplate_subject_values_idx',
     'type': 'KeywordIndex', },
    {'name': 'smtemplate_section_idx',
     'type': 'FieldIndex', },
    {'name': 'smtemplate_suppl_category_idx',
     'type': 'KeywordIndex', },
)

catalog_columns = (
    'lastname',
    'smtemplate_subject_values_idx',
    'smtemplate_section_idx',
    'smtemplate_suppl_category_idx',
    'exclude_from_mobile_nav',
    )

purge_existing_indexes = ()
purge_existing_columns = ()

def setup_indexes(portal, indexes, columns, purge_indexes=(), purge_columns=()):
    ct = getToolByName(portal, 'portal_catalog')

    new_metadata = False

    for idx in indexes:
        if idx['name'] in purge_indexes and idx['name'] in ct.indexes():
            ct.delIndex(idx['name'])
        if idx['name'] in ct.indexes():
            print "Found the '%s' index in the catalog, nothing changed.\n" % idx['name']
        else:
            ct.addIndex(**idx)
            print "Added '%s' (%s) to the catalog.\n" % (idx['name'], idx['type'])
    for entry in columns:
        if entry in purge_columns and entry in ct.schema():
            ct.delColumn(entry)
        if entry in ct.schema():
            print "Found '%s' in the catalog metadatas, nothing changed.\n" % entry
        else:
            ct.addColumn(entry)
            print "Added '%s' to the catalog metadatas.\n" % entry
            new_metadata = True
    if new_metadata:
        print "Reindexing catalog... "
        ct.refreshCatalog(clear=0)
        print "Done.\n"

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('policy_various.txt') is None:
        return

    # Add additional setup code here
    portal = context.getSite()

    # Create indexes
    setup_indexes(portal=portal,
                  indexes=catalog_indexes,
                  columns=catalog_columns)

def setupVariousDemoContent(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('policy_demo_content.txt') is None:
        return

    # Add additional setup code here
    portal = context.getSite()

    # EMPTY SO FAR.
