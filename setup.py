import re
from setuptools import setup

description = 'Ello Dev Utils'

setup(
    name='ElloDevUtils',
    version='0.0.1-dev',
    #url='https://github.com/peritus/bumpversion',
    author='Clayton A. Alves',
    author_email='clayton.aa@gmail.com',
    license='MIT',
    packages=['ello_dev_utils'],
    description=description,
    entry_points={
        'console_scripts': [
            'ordena-uses = ello_dev_utils.ordena_uses:main',
            'configure = ello_dev_utils.configure:main',
        ]
    }
)
