# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

version_file = os.path.join('Products', 'SignupSheet', 'version.txt')
version = file(version_file).read().strip()
desc = file('README.txt').read().strip()
changes = file('CHANGES.txt').read().strip()

long_description = desc + '\n\nCHANGES\n=======\n\n' +  changes 

setup(name='Products.SignupSheet',
      version=version,
      license='GPL2',
      author='Aaron VanDerlip and others',
      author_email='avanderlip@gmail.com',
      maintainer='RedTurtle Technology',
      maintainer_email='sviluppoplone@redturtle.it',
      classifiers=[
                   'Programming Language :: Python',
                   'Framework :: Zope2',
                   'Framework :: Plone',
                   'Framework :: Plone :: 3.3',
                   'Development Status :: 4 - Beta',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
      ],
      keywords='Archetypes Plone Zope Python PloneGov', 
      url='http://plone.org/products/signupsheet',
      description="A signup sheet implementation for Plone",
      long_description=long_description,
      packages=['Products', 'Products.SignupSheet'],
      install_requires=('setuptools',
                        'Products.ATSchemaEditorNG', 
                        'Products.TALESField', 
                        'Products.TemplateFields'),
      include_package_data = True,
      zip_safe=False,
      namespace_packages=['Products'],
      )
