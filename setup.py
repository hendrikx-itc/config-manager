from distutils.core import setup

setup(
    name='config_manager',
    version='0.1.0',
    packages=['config_manager'],
    install_requires=[
        'PyYAML', 'jinja2', 'sphinx'
    ],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'config = config_manager.config:main'
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
