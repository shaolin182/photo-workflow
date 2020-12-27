from setuptools import setup, find_packages

setup(
    name='photo-workflow',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click', 'pyyaml', 'py3exiv2'
    ],
    entry_points='''
        [console_scripts]
        photo-workflow=photo_workflow.workflow:cli
    ''',
)
