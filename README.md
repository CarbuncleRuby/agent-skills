# agent-skills

Agent Skills originally written for a personal agent setup, scrubbed and
generalized for public use. Each skill is self-contained: valid Agent Skills
frontmatter, no personal data, no environment-specific paths.

| Skill | What it is |
|---|---|
| `verify-quote-in-media-archive` | Check whether a creator/speaker ever said something, via archived transcripts — with context checks, ASR-variant handling, and coverage-honest negative reporting. |
| `bundled-data-sync` | Keep a dataset consistent across duplicated bundles (app, workers, replay engine), with content-hash archives so saved replays keep working. Includes a sync-script skeleton. |
| `delegated-work-supervision` | Supervision contract for detached processes and delegated work: launch checks, exit watchers with stated limits, hang detection, retry cutoffs, verify-before-report. |
| `form-submission-safety` | Submit web forms carrying the user's personal data on their behalf: verify the organizer and official route, survey before collecting, minimal data, CAPTCHA and proxy-entry rules, per-submission confirmation, entry records. Sweepstakes entry is the worked example. |

## License

MIT — see [LICENSE](LICENSE).
