from distutils.core import setup

setup(
    name='config_manager',
    version='0.1',
    packages=['config_manager'],
    install_requires=[
        'PyYAML'
    ],
    package_dir={'': 'src'},
    scripts=[
        'scripts/render-config'
    ],
    url='',
    license='GPL',
    author='Alfred Blokland',
    author_email='alfred.blokland@hendrikx-itc.nl',
    description='Configuration Manager'
)
