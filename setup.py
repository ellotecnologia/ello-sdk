from setuptools import setup, find_packages

description = 'Ello SDK'

setup(
    name='Ello SDK',
    version='0.0.5',
    author='Clayton A. Alves',
    author_email='clayton.aa@gmail.com',
    license='MIT',
    packages=find_packages(),
    description=description,
    install_requires = [
        'fdb==1.8',
        'dokuwikixmlrpc',
        'requests',
        'telepot==12.5',
        'colorama==0.3.9',
        'pyperclip',
        'sqlparse==0.2.4',
        'Pygments==2.2.0',
        'telepot==12.5',
        'future==0.16.0',
        'configparser'
    ],
    dependency_links=['git@github.com/kynan/dokuwikixmlrpc.git@0a01d6af2c8ff26acccbd1826b0c5ac9ca28a6a1'],
    entry_points={
        'console_scripts': [
            'ell=ello.cli.ell:main',
            'ordena-uses=ello.cli.ordena_uses:main',
            'configure=ello.cli.configure:main',
            'dof=ello.cli.dof:main',
            'fbtrace=ello.cli.fbtrace:main'
        ]
    },
    include_package_data=True
)
