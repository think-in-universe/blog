### Introduction

`blog` is a blog builder that syncs steem blogs into GitHub pages, or other blog services if you need. It's built based on steem APIs and [hexo](https://hexo.io) blog framework.

![Pixabay](https://cdn.pixabay.com/photo/2013/10/31/13/43/manuscript-203465_1280.jpg)
<br/>
Image Source: [Pixabay](https://cdn.pixabay.com/photo/2013/10/31/13/43/manuscript-203465_1280.jpg)


### Features

1. Synchronize posts from steem by account, tags, time, etc. to the GitHub pages daily.
1. With the help of hexo themes, the blog is easier to read, search, archive, etc.

You can find my blog from [https://think-in-universe.github.io/blog](https://think-in-universe.github.io/blog) as an example.


### Installation

If you want to install the service locally, you should follow the steps below.

The python packages in this project is managed with `pipenv` so you need to run below commands to install the packages.

``` bash
pip install pipenv
pipenv install
```

Also, you need to install hexo themes and packages with the below commands.

```bash
npm install -g hexo-cli
npm install
```


### Commands

The commands / tasks in this project is manged with `invoke` package.

By running `pipenv run invoke -l`, you're able to see the available tasks in the bot.

``` bash
Available tasks:

  blog.build         build the static pages from steem posts
  blog.deploy        deploy the static blog to the GitHub pages
  blog.download      download the posts to local by the account
  blog.test          build and launch blog server in local environment
  steem.list-posts   list the post by account, tag, keyword, etc.
```

To see the introduction of a command, run `pipenv run invoke -h <command>`.


### How to Launch the Blog

First, fork this project to your GitHub account.

Second, you need to update some user profile info in the `_config.yml` and `_config.theme.yml` files manually (we didn't modify the two files with steem data automatically), espcially the following fields:

`_config.yml`

```
title
author
language
url
deploy
  repository
```

`_config.theme.yml`

```
author
author_title
location
avatar
follow_link
social_links
```

After you edited the user profile, commit and push the latest file to your `blog` repository. Then, you can launch the blog either locally or remotely in GitHub.


#### Method 1: Build the blog server locally for your account.

``` bash
pipenv run invoke blog.download -a <account>
pipenv run invoke blog.test

```

The blog server will be launched at http://localhost:4000/blog/

To build blog server for tags, use the parameter `-t <tag>` instead.


#### Method 2: Push the blog server to GitHub pages

``` bash
pipenv run invoke blog.download -a <account>
pipenv run invoke blog.deploy

```

The blog server will be pushed to the GitHub pages you specified in `_config.yml` file, such as `https://<username>.github.io/blog`


#### Method 3: Sync the blogs daily with Travis CI

You can also use http://travis-ci.org service to sync your blog daily with your Steem account.

To enable this, login into your travis account, then follow the following steps:

1. Enable your `blog` repository in Travis CI.
2. In the setting page of `blog`, add the environment variables for your `GIT_EMAIL`, `GIT_USERNAME`, [`GITHUB_PAT`](https://github.com/settings/tokens), `STEEM_ACCOUNT`
3. Then in `Cron Jobs`, add the daily job on `master` branch.

That's it. Then your blog will be synchronized into your GitHub pages at `https://<username>.github.io/blog` daily.


### Reference

- The interaction with Steem blockchain is built with [beem](https://github.com/holgern/beem) project.
- The blog generation is built with [hexo](https://hexo.io) blog framework.


### License

The project is open sourced under MIT license.
