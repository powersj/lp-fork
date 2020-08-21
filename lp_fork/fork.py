# This file is part of lp-fork. See LICENSE file for license info.
"""Fork module."""

import logging
import os
import sys

import git
from launchpadlib.credentials import UnencryptedFileCredentialStore
from launchpadlib.launchpad import Launchpad

from .progress import Progress

logging.getLogger("git").setLevel(logging.WARNING)


class Fork:
    """Fork class.

    Accepts URLs in the form of:

        * https://git.launchpad.net/cloud-init
        * git+ssh://lp_user@git.launchpad.net/cloud-init

    Cloning other users' repos will have the "~" in them, which makes finding
    the destination a little less straightforward.

    If a user has the "lp:" shortcut setup then those are also supported:

        * lp:cloud-init

    The "git://" URLs are not supported.
    """

    def __init__(self, repo_url):
        """Initialize fork class."""
        self._log = logging.getLogger(__name__)
        self._lp = self._lp_login()
        self.lp_user = self._lp.me.name

        self.repo_name = repo_url.split("/")[-1].split(":")[-1]
        self.repo_url = repo_url

        self.fork_path = "~%s/%s" % (self.lp_user, self.repo_name)
        if "~" in repo_url:
            suffix = "/".join(repo_url.split("~")[-1].split("/")[1:])
            self.fork_path = "~%s/%s" % (self.lp_user, suffix)
        self.fork_url = "git+ssh://%s@git.launchpad.net/%s" % (
            self.lp_user,
            self.fork_path,
        )

        self._verify_url()

    def create_fork(self):
        """Create personal fork of given repo.

        Clone the upstream repo, then create the new remote and push.
        This will also set the default branch if necessary.
        """
        self._log.info(u"\U0001F374 Forking Launchpad Repo")
        self._log.info("src: %s\ndst: lp:%s" % (self.repo_url, self.fork_path))

        repo = self._git_clone()
        self._git_remote(repo)

    def _git_clone(self):
        """Git clone a repo to specific directory."""
        try:
            os.mkdir(self.repo_name)
        except FileExistsError:
            self._log.error("Oops: Local destination direcotry already exists")
            sys.exit(1)

        try:
            return git.Repo.clone_from(
                self.repo_url, self.repo_name, progress=Progress()
            )
        except git.exc.GitCommandError as exception:
            os.rmdir(self.repo_name)
            self._log.error("Oops: Failed to clone repo. Bad URL?")
            self._log.debug(exception.stderr)
            sys.exit(1)

    def _git_remote(self, repo):
        """Setup and push remote fork."""
        remote = repo.create_remote(self.lp_user, self.fork_url)

        try:
            remote.push(progress=Progress())
        except git.exc.GitCommandError as exception:
            self._log.error("Oops: Failed to push fork")
            self._log.debug(exception.stderr)
            sys.exit(1)

        remote.fetch()

    @staticmethod
    def _lp_login():
        """Login to Launchpad and return LP object.

        For additional docs see the online API Docs:
        https://launchpad.net/+apidoc/devel.html
        """
        credential_store = UnencryptedFileCredentialStore(
            os.path.expanduser("~/.lp_creds")
        )
        return Launchpad.login_with(
            "lp-fork", "production", version="devel", credential_store=credential_store,
        )

    def _verify_url(self):
        """Verify the URL uses the right protocol."""
        if self.repo_url.startswith("git://"):
            self._log.error("Oops: git:// is unsupported. Use https:// or git+ssh://")
            sys.exit(1)
        elif not (self.repo_url.startswith(("git+ssh://", "https://", "lp:"))):
            self._log.error("Oops: unknown URL protocol. Use https:// or git+ssh://")
            sys.exit(1)
