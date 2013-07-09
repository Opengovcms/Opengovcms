# -*- extra stuff goes here -*-

import os
from OFS.Image import File
from Products.CMFCore.utils import getToolByName 
from Products.Five.browser import BrowserView
from logging import getLogger
from shutil import rmtree
from subprocess import Popen, PIPE
from tempfile import mkdtemp
from zope.component import getGlobalSiteManager
from zope.component.interfaces import ObjectEvent
from zope.event import notify
from zope.interface import Interface
from zope.interface import implements

logger = getLogger('smtemplate.theme')

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), 'static')
RESOURCES = {
    'less/styles.less': 'css/styles.css',
    'less/tinymce.less': 'css/tinymce.css',
}

class IThemeChangedEvent(Interface):
    """"""


class ThemeChangedEvent(ObjectEvent):
    """"""
    implements(IThemeChangedEvent)


def dump(dir, prefix):
    for name in dir.listDirectory():
        relativeName = os.path.join(prefix, name)
        if dir.isDirectory(name):
            os.mkdir(relativeName)
            dump(dir[name], relativeName)
        elif dir.isFile(name):
            f = open(relativeName, "w")
            f.write(dir.readFile(name))
            f.close()

def readCSS(prefix, css_file):
    f = open(os.path.join(prefix, css_file))
    data = f.read()
    f.close()
    return data


def getLessCompiler():
    lessc = os.path.join(os.environ.get('INSTANCE_HOME'), os.path.pardir, os.path.pardir, 'bin', 'lessc')
    if not os.path.exists(lessc):
        logger.error("A valid lessc executable cannot be found. "
                     "We are assumming that it has been provided by buildout "
                     "and placed in the buildout bin directory. "
                     "If not, you should provide one (e.g. symbolic link) and place it there.")
        return
    return lessc


class CompileErrors(Exception):
    pass


def renderLESS(lessc_command_line, file_less, file_css):
    logger.info("The '%s' has been compiled to '%s'." % (file_less, file_css))
    # Call the LESSC executable
    process = Popen([
            lessc_command_line,
            file_less,
            file_css
        ], stdout=PIPE, stderr=PIPE)
    output, errors = process.communicate()
    # Return the command output
    if output:
        logger.info("Info on compile: %s" % output)
    if errors:
        logger.error("Error on compile: %s" % errors)
        raise CompileErrors(errors)
    return output


def subscriber(theme, event):
    for less_resource in RESOURCES:
        if not theme.isFile(less_resource):
            return
    lessc = getLessCompiler()
    if not lessc:
        return
    prefix = mkdtemp()
    dump(theme, prefix)
    for less_resource in RESOURCES:
        file_less = os.path.join(prefix, less_resource)
        if not os.path.exists(file_less):
            continue
        css_file = RESOURCES[less_resource]
        file_css = os.path.join(prefix, css_file)
        renderLESS(lessc, file_less, file_css)
        if not os.path.exists(file_css):
            continue
        theme.writeFile(css_file, readCSS(prefix, css_file))
    rmtree(prefix)
    exportdir = os.environ.get('EXPORT_THEME_DIR')
    if exportdir and os.path.exists(exportdir):
        themedir = os.path.join(exportdir, theme.__name__)
        if os.path.exists(themedir):
            rmtree(themedir)
        os.mkdir(themedir)
        dump(theme, themedir)
        f = open(os.path.join(themedir, "AUTHOR"), "w")
        portal_membership = getToolByName(theme, 'portal_membership')
        f.write(portal_membership.getAuthenticatedMember().getUserName())
        f.close()


getGlobalSiteManager().registerHandler(subscriber, (Interface, IThemeChangedEvent))


def writeFile(self, path, data):
    self._old_writeFile(path, data)
    if path.endswith(".less"):
        notify(ThemeChangedEvent(self))
