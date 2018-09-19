from setuptools import setup

setup(name='rest-monitor',
      version='0.1',
      description='REST based network monitor that allows the configuration of services that listen over a REST API and trigger actions as needed',
      url='https://github.com/wontoniii/rest-monitor',
      author='Francesco Bronzino',
      author_email='wontoniii@gmail.com',
      license='GNU',
      packages=['nm'],
      install_requires=['igraph'],
      zip_safe=False)

