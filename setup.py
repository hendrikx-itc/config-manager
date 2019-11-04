from distutils.core import setup

setup(
    name='config_manager',
    version='0.1.0',
    install_requires=[
        'PyYAML', 'jinja2', 'sphinx', 'gitpython'
    ],
    package_dir={'': 'src'},
    packages=[
        'config_manager',
        'config_manager.rst'
    ],
    entry_points={
        'console_scripts': [
            'config = config_manager.command:main'
        ]
    },
    package_data={
        'config_manager': ['doc_template']
    },
    url='',
    license='GPL',
    author='Alfred Blokland',
    author_email='alfred.blokland@hendrikx-itc.nl',
    description='Configuration Manager'
)
