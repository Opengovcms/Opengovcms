Starting a new project
======================

Headnet specific tasks has been marked "Headnet:" in the buildout files.

Use svn cp to copy the buildout to preserve svn properties.

Remove the file cron.d/template before rolling out on production for the first time.

Upgrading to a new plone version
================================

When upgrading, don't copy the plone and zope versions files uncritically:
We uncomment the pinning of zc.buildout, setuptools, distribute. So take a diff first.

When making a new version of this standard buildout, use svn cp, not import/export. That way svn properties, externals etc.
are also copied.

The plone version is specified in a few places: 
The plone4_versions.cfg of course, but also in find-links in base.cfg

Also check base_sources.cfg - it might need to be updated from git://github.com/plone/buildout.coredev - the proper branch.

Use ./bin/yolk -U when updating to check for new versions of non-plone standard packages. Update development tools to 
new versions, etc.

