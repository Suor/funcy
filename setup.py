from setuptools import setup

setup(
    name='funcy',
    version=open('VERSION').read().strip(),
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='A fancy and practical functional tools',
    long_description=open('README.rst').read(),
    url='http://github.com/Suor/funcy',
    license='BSD',

    packages=['funcy'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ]
)
