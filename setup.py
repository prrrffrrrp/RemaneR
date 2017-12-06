from setuptools import setup, find_packages

setup(name='remaner',
      version='0.1',
      description='File renamer where the new names are supplied from a file.',
      url='https://github.com/prrrffrrrp/RemaneR',
      author='prrrf',
      author_email='prrrffrrrp@gmail.com',
      license='MIT',
      keywords='rename renamefiles renamefromfile cool cli notboring',
      packages=find_packages(exclude=['tests']),
      install_requires =['textract', 'docopt', 'colorama'],
      python_requires='>=3',
      zip_safe=False)
