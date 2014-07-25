from setuptools import setup

from os import path as op
CURRENT_DIR = op.dirname(__file__)

__version__ = '0.0.1'

setup(
    name='ubackup',
    version=__version__,
    packages=['ubackup'],

    install_requires=open(op.join(CURRENT_DIR, 'requirements.txt')).read().splitlines(),

    author='Thomas Kliszowski',
    author_email='contact@thomaskliszowski.fr',
    description='Minimalist backup tool',
    license='MIT',
    keywords='ubackup backup tool',
    url='https://github.com/ThomasKliszowski/ubackup',
    include_package_data=True,
    zip_safe=False,
    entry_points='''
        [console_scripts]
        ubackup=ubackup.cli:main
    '''
)
