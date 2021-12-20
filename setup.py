from setuptools import setup


# Remove build status and move Gitter link under title for PyPi
README = open('README.rst').read()    \
    .replace('|Build Status|', '', 1) \
    .replace('|Gitter|', '', 1)       \
    .replace('===\n', '===\n\n|Gitter|\n')


setup(
    name='funcy',
    version=open('VERSION').read().strip(),
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='A fancy and practical functional tools',
    long_description=README,
    url='http://github.com/Suor/funcy',
    license='BSD',

    packages=['funcy'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ]
)
