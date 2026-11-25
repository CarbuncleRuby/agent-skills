# agent-skills


Agent Skills originally written for a personal agent setup, scrubbed and

generalized for public use. Each skill is self-contained: valid Agent Skills

frontmatter, no personal data, no environment-specific paths.


| Skill | What it is |

|---|---|

| `verify-quote-in-media-archive` | Check whether a creator/speaker ever said something, via archived transcripts — with context checks, ASR-variant handling, 
and coverage-honest negative reporting. |

| `bundled-data-sync` | Keep a dataset consistent across duplicated bundles (app, workers, replay engine), with content-hash archives so saved replays keep 
working. Includes a sync-script skeleton. |

| `delegated-work-supervision` | Supervision contract for detached processes and delegated work: launch checks, exit watchers with stated limits, hang 
detection, retry cutoffs, verify-before-report. |

| `form-submission-safety` | Submit web forms carrying the user's personal data on their behalf: verify the organizer and official route, survey before 
collecting, minimal data, CAPTCHA and proxy-entry rules, per-submission confirmation, entry records. Sweepstakes entry is the worked example. |

| `experiment-record-standard` | Set up experiment records from day one so results stay traceable and reusable: a claims ledger with confirmation status (confirmatory / exploratory / retracted), canonical run JSONs, a term registry with stable IDs, a decision log kept separate from the work log, and a retracted-expressions list. Includes the full standard and templates for the five records. |
| `paper-introduction` | Introduce a paper in chat with a fixed-format card (title, authors and affiliations, a concrete labelled date, the abstract translated into the user's preferred language), then the explanation outside the card. |
| `responsive-mobile-layout` | Phone-first web layout that fits the device: dvh fit-screens with one flex absorber, safe-area padding, fluid type, overflow prevention, and the rule that state changes never change geometry. |


## License


MIT — see [LICENSE](LICENSE).
