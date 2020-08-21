# This file is part of lp-fork. See LICENSE file for license info.
"""Progress modules.

The SpinnerCounter and Progress classes were based on those found in the
Braiins_OS repo file. You can find this here:

https://github.com/Cminers/braiins-os/blob/master/builder/repo.py

Copyright (C) 2018  Braiins Systems s.r.o.
"""

import git
from progress.bar import Bar
from progress.spinner import Spinner


class SpinningCounter(Spinner):
    """Spinner that counts class."""

    def __init__(self, prefix, **kwargs):
        """Initialize spinning counter."""
        super().__init__(prefix, **kwargs)
        self.count = 0

    def next(self, n=1):
        """Add value to current count."""
        self.count += n
        super().next()

    def write(self, s):
        """Add value of count after the prefix and spinner."""
        super().write(" %s %s" % (s, self.count))


class Progress(git.RemoteProgress):
    """Class to keep track of git action progress."""

    OPCODE_STRINGS = {
        git.RemoteProgress.CHECKING_OUT: "Checking out files",
        git.RemoteProgress.COMPRESSING: "Compressing objects",  # 8
        git.RemoteProgress.COUNTING: "Counting objects",  # 4
        git.RemoteProgress.FINDING_SOURCES: "Finding sources",  # 128
        git.RemoteProgress.RECEIVING: "Receiving objects",  # 32
        git.RemoteProgress.RESOLVING: "Resolving deltas",  # 64
        git.RemoteProgress.WRITING: "Writing objects",  # 16
    }

    def __init__(self):
        """Initialize Progress class."""
        super().__init__()
        self._progress = None
        self._last_count = 0

    def update(self, op_code, cur_count, max_count=100.0, message=""):
        """Update the current progress status."""
        cur_count = int(cur_count)
        max_count = max_count and int(max_count)
        op_id = op_code & self.OP_MASK
        stage_id = op_code & self.STAGE_MASK

        if stage_id & self.BEGIN:
            op_msg = self.OPCODE_STRINGS[op_id]

            # On the first stage, no max_count so use the spinner to count
            if max_count:
                self._progress = Bar(op_msg, max=max_count)
                self._last_count = 0
            else:
                self._progress = SpinningCounter(op_msg)

        self._progress.next(n=cur_count - self._last_count)
        self._last_count = cur_count

        # Clear the line after each stage, except the last one, add new line.
        if stage_id & self.END:
            # git.remote.RemoteProgress.RESOLVING
            if op_id == 64:
                self._progress.finish()
            else:
                self._progress.clearln()
