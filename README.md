# Launchpad Fork

Clone and create forks of Launchpad repos.

## Usage

All that is necessary is to provide the url to the git repo the user wishes to fork:

```shell
lp-fork https://git.launchpad.net/curtin
```

Accepts URLs in the form of:

* https://git.launchpad.net/curtin
* git+ssh://$LP_USER@git.launchpad.net/curtin
* lp:curtin
* lp:~ubuntu-core-dev/ubuntu-seeds/+git/ubuntu

The "lp:" shortcut can be setup in the user's `.gitconfig` by adding the following:

```shell
[url "git+ssh://powersj@git.launchpad.net/"]
    insteadof = lp:
```

The "git://" URLs are *not* supported.

## Remotes

After creating the fork the user will be left with the `origin` set to the original upstream location and a `$LP_USER` remote for the fork. Here is an example:

```shell
$ lp-fork lp:curtin
🍴 Forking Launchpad Repo
src: lp:curtin
dst: lp:~powersj/curtin
Resolving deltas |################################| 17390/17390
Resolving deltas |################################| 220/220
$ cd curtin
$ git remote -v
origin  git+ssh://powersj@git.launchpad.net/curtin (fetch)
origin  git+ssh://powersj@git.launchpad.net/curtin (push)
powersj git+ssh://powersj@git.launchpad.net/~powersj/curtin (fetch)
powersj git+ssh://powersj@git.launchpad.net/~powersj/curtin (push)
```
