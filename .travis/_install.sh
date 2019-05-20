#!/bin/sh

set -e

[ "${TRAVIS_BRANCH}" != "master" ] && exit 0

pipenv install --pypi-mirror https://pypi.python.org/simple

# install hexo commands
npm install

