---
name: delegated-work-supervision
description: Supervise work that leaves the main session — detached processes (nohup, SSH launches, cron), subagent delegations, and browser delegations — so nothing finishes, fails, or hangs in silence. Use when launching a detached or remote process, delegating a multi-step task, or reporting on delegated work. Covers launch checks in the target environment, exit watchers with stated limits, hang detection, retry cutoffs in delegation briefs, and verifying returned work before reporting it.
---

# Delegated and detached work supervision

Work that leaves the main session fails silently by default: a detached
process finishes and nobody reports it, a delegate repeats one failing move
for an hour, a launch dies instantly in an environment whose PATH differs
from the interactive shell. This skill is the supervision contract that
prevents those three failures.

## 1. Prefer tracked execution over detaching

- Use a runtime-tracked background task rather than a detached process when
  the platform offers one, because its completion already returns to you
  without a separate watcher.
- Keep short work in the main session instead of detaching it: supervision
  costs more than the run saves.

## 2. Launch checks (for anything you do detach)

Non-interactive shells (SSH without a login shell, `nohup`, cron) do not
inherit the interactive PATH. Most "tool not installed" and "process never
started" failures are born here.

- Resolve each binary in the same shell type that will run it, not in your
  interactive session. Compare the two views when in doubt:
  `ssh host 'command -v ffmpeg; echo $PATH'` (non-interactive) vs.
  `ssh host 'zsh -lc "command -v ffmpeg"'` (login shell). Check standard
  locations directly (`/usr/sbin`, `/usr/local/bin`, `/opt/homebrew/bin`,
  user bin directories) before saying a tool is not installed, and name the
  environment and locations checked when you report one missing.
- Launch with the absolute path the target environment resolved.
- Verify the launch actually started, shortly after starting it: the
  process exists, its log file exists and is growing, or its first expected
  output appeared. Also check for the opposite failure — a process that
  exited immediately with status zero and left a static log. A launch with
  no process and no growing log is a failed launch: read the startup error
  or fix the path before relaunching, and do not report it as started.
- When safe, run the command in the foreground for a few seconds first; its
  startup errors name the missing binary or path directly.

## 3. Pair every detached run with a watcher

- Pair any process you detach with a watcher from the start: a tracked
  background shell that waits for the process to exit and returns the tail
  of its log. Skeleton:

  ```sh
  while kill -0 "$PID" 2>/dev/null; do sleep 30; done
  echo "process $PID exited"; tail -n 40 run.log
  ```

  (For a process on another machine, run the same loop over SSH, or poll
  `ssh host "kill -0 $PID"` from the watcher side.)
- State the expected duration at launch, and tell the user the watcher
  exists and its limits: a watcher that itself fails returns to silence,
  its notice lags by its polling interval, and **it cannot detect a hang**.
- Hang detection is your job, not the watcher's: when a watched run stays
  silent past twice its expected duration, go and look — process state, and
  whether the log file's modification time has stopped advancing.
- Report the completion when the watcher fires, with the log tail or result
  it returned, rather than leaving a finished run unreported until the user
  asks.

## 4. Bound the retries in every delegation brief

Delegates repeat a failing approach far past the point of usefulness (one
real case: an hour of scrolling variations for a button that a single page
reload would have rendered). Write the cutoff into the brief itself, e.g.:

> "If an element cannot be reached or does not render, give up on that
> approach after a few tries and switch to the named fallback (reload the
> page, or another route). If the fallback also fails, stop and report back
> early instead of continuing to repeat variations."

- Name the fallback in the brief, and require early escalation when the
  fallback also fails.
- Treat long repetition of the same small move as wasted time to cut off,
  not as persistence to praise.

## 5. Verify returned work before reporting it

- Check that delegated work actually finished before you report it as
  done: open the deliverable, read the changed state, or run the check the
  task defined. A delegated report can leave work silently unfinished.
- Inspect any structured artifact a delegate hands back (a link, a token,
  an embedded widget, a file reference) before forwarding it to the user:
  confirm what it actually contains and that it is still current. Never
  forward an artifact whose contents you could not check — a stale one can
  resurface choices the user already made and decided.

## 6. Report the supervision state

- Separate your completion report into: what the delegate or process
  produced, what you verified yourself, and what remains unverified or
  still running.
- Surface a failed watcher, a cut-off retry loop, or an unfinished delegate
  result as soon as you find it, with the next step you will take.
