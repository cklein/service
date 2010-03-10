import sys, os
try:
    from setuptools import setup
    kw = {'entry_points':
          """[console_scripts]\nconfig = config:main\n""",
          'zip_safe': False}
except ImportError:
    from distutils.core import setup
    if sys.platform == 'win32':
        print 'Note: without Setuptools installed you will have to use "python -m config PARAMETERS"'
    else:
        kw = {'scripts': ['scripts/config']}
import re

setup(name='service',
      version='0.1',
      description="Supervise directory structure builder",
      long_description="ADD ME!",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
      ],
      keywords='',
      author='Christian Klein',
      author_email='c.klein@hudora.de',
      url='http://github.com/cklein/service',
      license='BSD',
      py_modules=['config'],
      **kw
      )
