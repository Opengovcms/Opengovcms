# -*- extra stuff goes here -*-

import os
from logging import getLogger
from subprocess import Popen, PIPE
from tempfile import mkdtemp
from shutil import rmtree
from Products.Five.browser import BrowserView
from OFS.Image import File
from zope.event import notify
from zope.interface import Interface
from zope.component.interfaces import ObjectEvent
from zope.interface import implements
from zope.component import getGlobalSiteManager

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
        relativeName = "%s/%s" % (prefix, name,)
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


def renderLESS(lessc_command_line, resource_path, resource_file_less, resource_file_css):
    logger.info("The '%s' has been compiled to '%s'." % (resource_file_less, resource_file_css))
    # Call the LESSC executable
    process = Popen([
            lessc_command_line,
            os.path.join(resource_path, resource_file_less),
            os.path.join(resource_path, resource_file_css)
        ], stdout=PIPE, stderr=PIPE)
    output, errors = process.communicate()
    # Return the command output
    if output:
        logger.info("Info on compile: %s" % output)
    if errors:
        logger.error("Error on compile: %s" % errors)
    return output

def subscriber(theme, event):
    prefix = mkdtemp()
    dump(theme, prefix)
    lessc = getLessCompiler()
    if not lessc:
        return
    for less_resource in RESOURCES:
        css_file = RESOURCES[less_resource]
        renderLESS(lessc, prefix, less_resource, css_file)
        theme.writeFile(css_file, readCSS(prefix, css_file))
    rmtree(prefix)


getGlobalSiteManager().registerHandler(subscriber, (Interface, IThemeChangedEvent))


def writeFile(self, path, data):
    self._old_writeFile(path, data)
    if path.endswith(".less"):
        notify(ThemeChangedEvent(self))
