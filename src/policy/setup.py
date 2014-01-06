from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='policy',
      version=version,
      description="Policy package for the SM template project",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='policy sm template plone',
      author='Thomas Clement Mogensen',
      author_email='tmog@headnet.dk',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          'plone.app.portlets',
          'plone.app.event',
          'plone.directives.form',
          'z3c.relationfield',
          'collective.dexteritytextindexer',
          'python-stdnum',
          'vobject',
          'plone.app.imagecropping',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
