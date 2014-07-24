from setuptools import setup

setup(name='zipa',
      version='1.00',
      platforms='any',
      description='General purpose REST API client',
      author='Vlad Temian & Calin Don',
      author_email='vladtemian@gmail.com',
      url='https://github.com/vtemian/zipa',
      packages=['zipa'],
      include_package_data=True,
      install_requires=['requests'],
      classifiers=[
          'Programming Language :: Python :: 2.7',
      ])
