Starting a new project
======================

Headnet specific tasks has been marked "Headnet:" in the buildout files.

Remove the file cron.d/template before rolling out on production for the first time.

Upgrading to a new plone version
================================

The plone version is specified in a few places: 
The plone4_versions.cfg of course, but also in find-links in base.cfg

Also check base_sources.cfg - it might need to be updated from git://github.com/plone/buildout.coredev - the proper branch.

Use ./bin/yolk -U when updating to check for new versions of non-plone standard packages. Update development tools to 
new versions, etc.

