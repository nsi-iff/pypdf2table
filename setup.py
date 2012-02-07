try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys, os

version = '0.2.2'

setup(
    name='pypdf2table',
    version=version,
    description="PDF table extraction tool",
    long_description=""" This project was based on the table extraction heuristic created by Burcu Yildiz, of
     Vienna Technological University
    """,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords='',
    author='Vanderson Mota dos Santos',
    author_email='vanderson.mota@gmail.com',
    url='http://nsi.iff.edu.br',
    license='',
    packages=find_packages(exclude=['ez_setup', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools', 'BeautifulSoup'],
    entry_points="""
    """,
)

