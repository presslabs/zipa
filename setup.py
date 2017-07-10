from setuptools import setup


setup(name='zipa',
      version="0.3.5",
      platforms='any',
      description='General purpose REST API client',
      author='Presslabs SRL',
      author_email='support@presslabs.com',
      url='https://github.com/Presslabs/zipa',
      packages=['zipa'],
      include_package_data=True,
      install_requires=['requests'],
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ])
