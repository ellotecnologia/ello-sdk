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
        'dokuwiki==1.2',
        'requests',
        'colorama==0.3.9',
        'pyperclip',
        'sqlparse==0.2.4',
        'Pygments==2.5.2',
        'telepot',
        'future==0.16.0',
        'configparser'
    ],
    entry_points={
        'console_scripts': [
            'ell=ello.cli.ell:main',
            'ordena-uses=ello.cli.ordena_uses:main',
            'configure=ello.cli.configure:main',
            'dof=ello.cli.dof:main',
            'fbtrace=ello.cli.fbtrace:main',
            'dfmgrep=ello.cli.dfmgrep:main',
            'dbgrep=ello.cli.dbgrep:main',
            'crgrep=ello.cli.crgrep:main',
            'crystal=ello.cli.crystal:main'
        ]
    },
    include_package_data=True
)
