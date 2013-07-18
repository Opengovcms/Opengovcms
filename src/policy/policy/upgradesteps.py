from logging import getLogger

log = getLogger('policy:upgrades')

def runProfiles(site, profile_ids):
    """ """
    setup_tool = getattr(site, 'portal_setup')

    for profile_id in profile_ids:
        if hasattr(setup_tool, 'runAllImportStepsFromProfile'):
            if not profile_id.startswith('profile-'):
                profile_id = "profile-%s" % profile_id
            setup_tool.runAllImportStepsFromProfile(profile_id)
        else:
            setup_tool.setImportContext(profile_id)
            setup_tool.runAllImportSteps()
        log.info("Ran profile " + profile_id)

def runDefaultProfile(tool):
    """ Run default profile """
    site = tool.aq_parent
    runProfiles(site, ('policy:default',))

def runDemoContentProfile(tool):
    """  """
    site = tool.aq_parent
    runProfiles(site, ('policy:demo_content',))

def installVocabManager(tool):
    """ Install ATVocabularyManager """
    site = tool.aq_parent
    runProfiles(site, ('Products.ATVocabularyManager:default',))

def installVersioningBeh(tool):
    """ Install ATVocabularyManager """
    site = tool.aq_parent
    runProfiles(site, ('plone.app.versioningbehavior:default',))

def installChimpfeed(tool):
    """ Install chimpfeed """
    site = tool.aq_parent
    runProfiles(site, ('collective.chimpfeed:default',))

def installCTaxonomy(tool):
    """ Install chimpfeed """
    site = tool.aq_parent
    runProfiles(site, ('collective.taxonomy:default',))

def importDefaultProfileRegistry(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:default', 'plone.app.registry',
        run_dependencies=False)

def importDefaultTypes(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:default', 'typeinfo',
        run_dependencies=False)

def importTinySettings(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:initialsetup', 'tinymce_settings',
        run_dependencies=False)

def importPortalTransforms(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:initialsetup', 'policy.portal_transforms',
        run_dependencies=False)

def migrateRegistry(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:migrate', 'plone.app.registry',
        run_dependencies=False)

def importPortalproperties(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:initialsetup', 'propertiestool',
        run_dependencies=False)
