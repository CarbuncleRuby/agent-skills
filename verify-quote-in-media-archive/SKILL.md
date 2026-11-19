---
name: verify-quote-in-media-archive
description: Verify whether a creator, streamer, podcaster, speaker, or lecturer ever said something in past videos, streams, or episodes — by searching archived transcripts, reading the context of every hit, and reporting coverage honestly. Use when asked "did X ever say Y", "find where X said …", or to check a remembered quote against an archive. A keyword hit alone is not evidence.
---

# Verify a quote in a media archive

## Define the claim and the archive scope

- Restate the claim in the user's own words and separate the exact phrase
  from paraphrases and related topics.
- Ask for a time window and any clue about the occasion when the user can
  give one, and record the window you actually check when they cannot.
- Build an archive list from the channel's public uploads, fan wikis, and
  episode lists before searching, and deduplicate the list.

## Get the transcripts

This is usually the hardest step; do it explicitly instead of assuming
transcripts exist.

- Prefer platform captions: for YouTube, `yt-dlp --write-auto-subs
  --skip-download <url>` fetches auto-captions without downloading the
  video. Respect the platform's terms and rate limits; fetch only what the
  search needs.
- Fall back to local speech recognition (e.g. Whisper) for items without
  captions, and note which items were transcribed this way — ASR text has
  different error modes than platform captions.
- Track how many archive items you obtained, how many you could search, and
  which ones you could not open.

## Search transcripts and check context

- Search for the exact phrase first, then expand to synonyms and related
  terms the speaker might have used.
- **Cover recognition variants.** Auto-captions and ASR misrecognize words,
  and in Japanese they vary kana/kanji forms and long-vowel spellings.
  Search likely misrecognitions and orthographic variants, not only the
  canonical phrase.
- **Read the surrounding context for every hit** and decide whether the
  speaker stated the claim, quoted a listener or comment, described a game
  or a third party, or repeated someone else's words. A keyword hit alone
  would falsely confirm a claim in exactly these cases — in one real check,
  the only exact-phrase hit turned out to be the speaker reading a
  listener's comment aloud.
- Keep the item link with a timestamp for each hit that supports the claim,
  and keep near misses separate from direct evidence.

## Report what the evidence does and does not prove

- Present a direct hit with its date, timestamp, and wording before
  presenting near misses.
- Report a negative result only for the archives you actually checked, and
  name the archives you could not check.
- List the gaps that keep a negative result from being absolute: members-only
  or deleted items, items without transcripts, appearances on other
  channels, and the share of the archive that has no searchable text.
- State the most likely source of a mixed memory when near misses explain
  it, and label that explanation as an inference rather than a fact.

## Ethics

- Check public statements only. Do not compile a profile of the person
  beyond the question asked, and do not publish findings about third parties
  without a separate, deliberate decision.

## Alternatives for better results

- Ask the user for a remembered occasion, companion, place, or wording when
  the first search finds only near misses, and search again with those
  clues.
- Check clips, fan wikis, and social posts when transcripts are missing,
  and treat those sources as secondary evidence rather than a transcript
  hit.
- Offer to check a user-supplied timestamp directly when a full item has no
  transcript, instead of claiming the whole item was watched.
