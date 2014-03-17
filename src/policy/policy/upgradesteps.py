from logging import getLogger
from Products.GenericSetup.upgrade import _upgrade_registry

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


def isInstalled(site, product_name):
    qi = getattr(site, 'portal_quickinstaller')

    installed_ids = [p['id'] for p in qi.listInstalledProducts()]
    if product_name in installed_ids:
        return True
    return False

# adapted from Products/GenericSetup/tool/manage_doUpgrades
def runUpgradeSteps(site, profile_id, product_name, check_installed=True):
    """Perform all available upgrade steps for profile_id.
    """
    log.info("Running available upgrade steps for profile " + profile_id)

    if check_installed and not isInstalled(site, product_name):
        log.info("Product %s is not installed in site" % str(product_name))
        return

    setup_tool = getattr(site, 'portal_setup')
    # These have not been run:
    steps_to_run = setup_tool.listUpgrades(u'Products.TinyMCE:TinyMCE')

    step = None
    for step_info in steps_to_run:
        step = _upgrade_registry.getUpgradeStep(profile_id, step_info['id'])
        if step is not None:
            step.doStep(setup_tool)
            msg = "Ran upgrade step '%s' for profile %s. Source: %s, dest: %s" % (
                                                step.title,
                                                profile_id,
                                                str(step.source),
                                                str(step.dest))
            log.info(msg)

    # We update the profile version to the last one we have reached
    # with running an upgrade step.
    if step and step.dest is not None and step.checker is None:
        setup_tool.setLastVersionForProfile(profile_id, step.dest)

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


def installPerson(tool):
    """ """
    site = tool.aq_parent
    runProfiles(site, ('collective.person:default',))


def installCTaxonomy(tool):
    """ """
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


def importActions(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:initialsetup', 'actions',
        run_dependencies=False)


def removePersonPortlet(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:migrate', 'portlets',
        run_dependencies=False)


def addSearchPortletsManager(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:migrate', 'portlets',
        run_dependencies=False)


def migratePortletsStep(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-policy:migrate', 'portlets',
        run_dependencies=False)


def updateSMRegistry(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-smtemplate.theme:default', 'plone.app.registry',
        run_dependencies=False)


def runProfilesForInitialSetup(tool):
    """ """
    site = tool.aq_parent
    runProfiles(site, (
        'policy:multilingual',
        'policy:multilingual-initial',
        'policy:publication-initial',
    ))

def runUpgradeStepsTiny(tool):
    """ """
    site = tool.aq_parent
    profile_id = u'Products.TinyMCE:TinyMCE'
    product_name = u'Products.TinyMCE'
    # Products installed at site creation time
    # like TinyMCE are not listed as installed in quickinstaller.
    # But for others it is best to be precautious and check if it is
    # installed before running an upgrade step. Use check_installed=True
    # in the normal case.
    runUpgradeSteps(site, profile_id, product_name, check_installed=False)

