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
        'fdb==1.8',
        'dokuwikixmlrpc==2010-07-19',
        'requests==2.7.0',
        'telepot==12.5',
        'colorama==0.3.9',
        'pyperclip==1.6.0',
        'sqlparse==0.2.4',
        'Pygments==2.2.0',
        'telepot==12.5',
        'future==0.16.0'
    ],
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
