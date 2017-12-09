from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='remaner',
      version='0.1',
      description='File renamer where the new names are supplied from a file.',
      long_description=long_description,
      url='https://github.com/prrrffrrrp/RemaneR',
      author='prrrf',
      author_email='prrrffrrrp@gmail.com',
      license='MIT',
      keywords='rename renamefiles renamefromfile cool cli notboring',
      packages=['app'],
      install_requires=['textract', 'docopt', 'colorama'],
      python_requires='>=3',
      scripts=['run.py'],
      zip_safe=False)
