---
name: paper-introduction
description: Introduce a paper in detail in chat by opening with a fixed-format card — paper title, authors with affiliations, a concrete publication date, and the abstract always translated into the user's preferred language — followed by the plain-language explanation and the context-specific answer outside the card. Use this whenever the user asks for a detailed introduction to, or explanation of, a specific paper (e.g. "introduce this paper in detail", "explain this paper to me"). Do not use it for saving a paper to the user's library (that is a paper-saving skill's job, if one exists), for a brief mention or a one-line reference to a paper, or for bibliographic lookup alone, or for a focused question about one part of a paper the user is already reading.
---

# Paper Introduction

The user reads paper introductions in two layers: the bibliographic facts first, in a fixed shape the user can scan, and the interpretation second, in ordinary prose. Mixing the two — or letting the abstract stay in a language the user has to work to read — forces the user to do the sorting work. This format was set on 2026-11-16, with two additions on 2026-11-18 (abstract always translated; date always concrete).

## The card

Open the reply with a card containing exactly these fields, in this order:

1. **Title** — the paper's title, in its original language.
2. **Authors and affiliations** — the authors with their affiliations, as the source gives them. Do not invent an affiliation that the source does not state.
3. **Publication date** — a **concrete date**, labelled, never just a year or a venue name. If a peer-reviewed version exists, give its date (journal: the online publication date; conference: the first day of the conference, labelled with the venue). If there is an arXiv version, also give its v1 submission date on the same line. For a preprint only, give the arXiv v1 date.
4. **Abstract** — a **faithful translation of the full abstract into the user's preferred language** (Japanese in the original use). Never paste the original into the card when it is in another language, and do not summarise: translation in the card, interpretation outside it. (For a paper already in the user's preferred language, the original abstract as-is.)

The card is a delimited block at the head of the reply; its medium (an in-chat card or a formatted text block) may follow the surface, but the fields, order, and language rules do not change.

## After the card

Continue **outside** the card, in ordinary chat text:

- A plain-language explanation of what the paper does and finds.
- The answer in the context the user asked from: how it relates to their research, how it compares to a paper already discussed, whether it is worth reading closely. This is where judgement goes; the card stays neutral facts.

## Source discipline

- Verify every card field at the **primary source** before writing: the arXiv abstract page, the publisher's page, or the paper PDF itself. Titles, author lists, affiliations, and dates copied from secondary summaries or search snippets have been wrong before.
- When the user asks for detail, read the body before explaining — at minimum the introduction, the method section, and the main results (including the key tables) — rather than expanding on the abstract alone.
- If the full text is not accessible (paywalled, unavailable), say so in the explanation and state which parts it is based on (abstract, publisher summary).
- If a field cannot be verified (an affiliation the source does not list, a date that is only a year), say so in the card rather than filling the gap with a guess.

## Boundaries

- Saving a paper is a different job: if a paper-saving skill exists, saving is its job; this skill covers only the introduction format. The two often pair: introduce with this format, save with that one when asked.
- A passing reference to a paper inside another answer does not need the card. The trigger is a detailed introduction of a specific paper.
