import pkg_resources

from plone.app.controlpanel.overview import OverviewControlPanel

class OverriddenOverviewControlPanel(OverviewControlPanel):
    def version_overview(self):

        core_versions = self.core_versions()
        versions = [
            'Plone %s (%s)' % (core_versions['Plone'],
                               core_versions['Plone Instance'])]

        versions.append(
            'SM Koncernskabelon version %s' %
            pkg_resources.get_distribution("policy").version
        )

        for v in ('CMF', 'Zope', 'Python'):
            versions.append(v + ' ' + core_versions.get(v))
        pil = core_versions.get('PIL', None)
        if pil is not None:
            versions.append('PIL ' + pil)
        return versions

