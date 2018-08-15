from setuptools import setup, find_packages
from wick import __version__

setup(name='wick',
      version=__version__,
      description='',
      long_description='',
      url='https://github.com/JoshuaSkelly/wick',
      author='Joshua Skelton',
      author_email='joshua.skelton@gmail.com',
      license='MIT',
      packages=find_packages(),
      scripts=['bin/wick'],
      keywords=[''],
      classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ])

