import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='working_calendar',
    version='0.0.1',
    author='Igor Iakovlev',
    author_email='igorxut@example.com',
    description='Utility for operate with working days.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/igorxut/working-calendar',
    packages=['working_calendar'],
    install_requires=[
        'typing',
    ],
    classifiers=(
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
