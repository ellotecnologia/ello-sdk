from setuptools import setup, find_packages

description = 'Ello Dev Utils'

setup(
    name='ElloDevUtils',
    version='0.0.3',
    author='Clayton A. Alves',
    author_email='clayton.aa@gmail.com',
    license='MIT',
    packages=find_packages(),
    description=description,
    install_requires = [
        'dokuwikixmlrpc==2010-07-19',
        'requests==2.7.0',
        'telepot==12.5'
    ],
    entry_points={
        'console_scripts': [
            'ell = ello_dev_utils.ell:main',
            'ordena-uses = ello_dev_utils.ordena_uses:main',
            'configure = ello_dev_utils.configure:main',
            'dof = delphi.dof:main',
        ]
    },
    include_package_data=True
)
