from setuptools import setup

import sys
if sys.version_info < (3, 6):
    sys.exit('Python < 3.6 is not supported')

setup(name='essentialjsonserializer',version='1.0.0',
      description='JSON serialization of complex python objects',
      classifiers=[
      'Development Status :: 1.0',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
      'Topic :: EssentialJSONSerializer :: Essential Data Science'],
     keywords='essentialjsonserializer',
     url='https://github.com/VermeirJellen/essentialjsonserializer_python',
     author='Jellen Vermeir',
     author_email='jellenvermeir@essentialdatascience.com',
     license='Proprietary',
     packages=['essentialjsonserializer'], package_dir = {'essentialjsonserializer': 'essentialjsonserializer'},
	  # dependency_links=['http://10.151.137.220:591/pypi/'],
	  install_requires=['numpy', 'pandas'],
	  include_package_data=True,
	  test_suite='nose.collector',
	  tests_require=['nose'],
      zip_safe=True)