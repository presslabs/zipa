from setuptools import setup

requires_list = [
    'coverage==3.7.1',
    'mock==1.0.1',
    'nose==1.3.0',
    'requests==1.2.3',
]

setup(name='papi',
      version='1.00',
      platforms='any',
      description='Universal REST API client',
      author='Vlad Temian & Calin Don',
      author_email='vladtemian@gmail.com',
      url='https://github.com/vtemian/papi',
      packages=['papi'],
      include_package_data=True,
      install_requires=requires_list,
      classifiers=[
          'Programming Language :: Python :: 2.7',
      ])
