from setuptools import setup

setup(
    name='funcy',
    version=open('VERSION').read().strip(),
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='A fancy and practical functional tools',
    long_description=open('README.rst').read().replace('|Build Status|', '', 1),
    url='http://github.com/Suor/funcy',
    license='BSD',

    packages=['funcy'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ]
)
