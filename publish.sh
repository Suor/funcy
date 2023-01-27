#!/usr/bin/bash

set -ex

NAME=funcy
VERSION=`cat VERSION`

python setup.py sdist bdist_wheel
twine check dist/$NAME-$VERSION*
twine upload --skip-existing -uSuor dist/$NAME-$VERSION*
