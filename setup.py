#!/usr-bin/env python

from distutils.core import setup

setup(name='Discourse-Map',
      version='1.0',
      description="A web scraper for Discourse that outputs the active users' location into a Google Spreadsheet which can be used by Zeemaps to display everyones location.",
      author='Matteus Magnusson',
      author_email='matteus.magnusson@gmail.com',
      url='https://github.com/Senth/discoursemap',
      packages=['discoursemap'],
      )