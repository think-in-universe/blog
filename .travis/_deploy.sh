#!/bin/sh

set -e

[ -z "${GITHUB_PAT}" ] && exit 0
[ "${TRAVIS_BRANCH}" != "master" ] && exit 0

git config --global user.email "${GIT_USERNAME}"
git config --global user.name "${GIT_EMAIL}"

git clone --depth 1 --branch gh-pages --single-branch https://${GITHUB_PAT}@github.com/${TRAVIS_REPO_SLUG}.git site
cd site
cp -r ../public/* ./

NOW=$(date +"%Y-%m-%d %H:%M:%S %z")
git add --all *
git commit -m "Site updated: ${NOW}" || true
git push -q origin gh-pages
