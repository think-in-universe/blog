#!/bin/sh

set -e

[ "${TRAVIS_BRANCH}" != "master" ] && exit 0

pipenv run invoke
