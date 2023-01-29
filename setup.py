from setuptools import setup


# Remove build status
README = open('README.rst').read().replace('|Build Status|', '', 1)


setup(
    name='funcy',
    version=open('VERSION').read().strip(),
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='A fancy and practical functional tools',
    long_description=README,
    long_description_content_type="text/x-rst",
    url='http://github.com/Suor/funcy',
    license='BSD',

    packages=['funcy'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ]
)
