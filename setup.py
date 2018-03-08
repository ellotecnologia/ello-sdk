from setuptools import setup, find_packages

description = 'Ello SDK'

setup(
    name='Ello SDK',
    version='0.0.4',
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
            'ell=ello.cli.ell:main',
            'ordena-uses=ello.cli.ordena_uses:main',
            'configure=ello.cli.configure:main',
            'dof=ello.cli.dof:main',
        ]
    },
    include_package_data=True
)
