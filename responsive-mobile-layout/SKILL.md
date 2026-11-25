---
name: responsive-mobile-layout
description: Lay out phone-first web screens (especially iOS Safari) so they fit the device instead of being fixed for one size — viewport-height fitting with dvh and flex absorption, fluid type with clamp(), safe-area padding, overflow prevention, and 44px tap targets. Use this whenever building or fixing a mobile web screen: a new app screen, a "doesn't fit / slightly scrolls / overflows sideways" report, or any screen that must show everything at once (quiz, player, feed controls). Do not use it for desktop-first data-dense tools, print styles, or native apps.
---

# Responsive Mobile Layout

These screens are opened almost exclusively on a phone. Screens built at one fixed size fail quietly: a few pixels of scroll on a screen that should be static, a sideways overflow from one long word, a toolbar that eats the bottom button. Build every phone screen so the *layout* absorbs the device's size, and verify the height budget before shipping. (The recipes below were verified in production, 2026-11-19.)

## Decide first: fit-screen or scroll-screen

- **Fit-screen** (quiz, player, game, anything where all controls must be visible at once): the root takes the exact viewport height and nothing scrolls. Use the fit recipe.
- **Scroll-screen** (feeds, lists, articles): content flows naturally; only guard against horizontal overflow and unreachable fixed elements. Use the scroll recipe.

## Fit-screen recipe

0. Reset the page first: `html, body { margin: 0; height: 100%; }` and `*, *::before, *::after { box-sizing: border-box; }`. The browser's default 8px body margin plus a `100dvh` root makes the page 16px taller than the viewport, and under the default `content-box` the root's padding adds on top of `100dvh` — both recreate the "slightly scrolls" bug this recipe exists to fix.
1. Root container: `height: 100dvh; display: flex; flex-direction: column; overflow: hidden; overscroll-behavior: none;`
   - Use **dvh**, never 100vh: Safari's collapsing toolbar makes 100vh taller than the visible area, which is exactly the "slightly doesn't fit" bug.
2. Every fixed part (header, bars, buttons, option lists) gets `flex: none`.
3. Exactly **one** element absorbs the slack: the main visual (card, board, stage) gets `flex: 1; min-height: 0`. Never give two elements flexible height, and never use a fixed `min-height` in px for the absorber — that reintroduces the overflow on short devices.
4. Bottom padding includes the home-indicator area: `padding-bottom: calc(14px + env(safe-area-inset-bottom))`. This only works if the page's viewport meta includes `viewport-fit=cover` — without it, `env(safe-area-inset-*)` returns 0: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`. In Next.js App Router: `export const viewport = { width: 'device-width', initialScale: 1, viewportFit: 'cover' }`.
5. Budget-check before shipping: sum the fixed parts (measure from the CSS) + the absorber's floor (~120px — budget arithmetic only; never write it as a CSS `min-height`, per step 3) and confirm it is under the smallest viewport you target; state the assumed height in the report (e.g. ~660px visible on a current iPhone in Safari — smaller iPhones in the 375×667pt class leave noticeably less). If it is over, shrink fixed parts (smaller paddings, smaller round buttons) — do not let the absorber go negative.

## Scroll-screen recipe

1. Content flows; cap line length with `max-width` on the column (640px works well) and 16px side padding.
2. Kill horizontal overflow at the cause, not the symptom:
   - Flex children that hold text need `min-width: 0`, or they refuse to shrink and push the row wide.
   - Long unbroken strings (URLs, long English words) need `overflow-wrap: anywhere` or ellipsis truncation (`white-space: nowrap; overflow: hidden; text-overflow: ellipsis` on a `min-width: 0` element).
   - `overflow-x: hidden` on the root is a last-resort guard, not the fix — if it is load-bearing, say so in the report.
3. Sticky headers/footers are fine; anything `position: fixed` at the bottom must add `env(safe-area-inset-bottom)` to its padding.

## Sizing rules

- **Fluid type for display text**: `font-size: clamp(min, vw-based, max)` (verified example: a quiz word at `clamp(30px, 9.5vw, 40px)`). Body text stays fixed (16px — also the threshold that stops iOS Safari from auto-zooming focused inputs; never set input font-size below 16px).
- **Tap targets ≥ 44px** in both dimensions (Apple HIG), with at least 8px between adjacent targets.
- Spacing on an 8px rhythm; screen-edge padding 16px.
- Numbers and counters that change width get `font-variant-numeric: tabular-nums` so the layout does not jitter.

## State changes never change geometry

An interactive element's states (selected, checked, correct, wrong, pressed, disabled, revealed) may only change **paint** properties: `color`, `background`, `border-color`, `box-shadow`, `opacity`, `transform`. Never change box metrics in a state: `border-width`, `padding`, `margin`, `width`/`height`, `font-size` — and not `font-weight` either (bold text is wider and can re-wrap, changing height). A state that changes size makes the whole screen jump at the exact moment the user is looking at it; this class of defect is easy to introduce and hard to notice in code review (one production case, 2026-11-19: a quiz option whose correct-state border went 1px → 2px and shifted every button below it).

- Need a thicker emphasis ring in one state? Keep the border at its base width and add the extra ring as `box-shadow: inset 0 0 0 1px <color>` — visually 2px, geometrically zero.
- Marks or labels that appear only in a state (○ / ✕, checkmarks, "saved" badges) get a **fixed-size slot from the start**: the slot's width/height is constant, only its content swaps. Never let an appearing element push siblings.
- `box-sizing: border-box` does not save you: with auto height, a thicker border still grows the box. The rule is constant metrics, not box-sizing.

## Known failure modes

- **100vh on Safari** → bottom content hidden under the toolbar or a few px of scroll. Fix: dvh (or svh when the small state is the safer assumption).
- **Flex child will not shrink** → row overflows sideways. Fix: `min-width: 0` (row direction) / `min-height: 0` (column direction) on the child.
- **Keyboard opens** → fit-screens collapse. Screens with text input should be scroll-screens, or scroll the focused field into view; never fight the keyboard with a fixed height.
- **Landscape / iPad** → a fit-screen designed for portrait gets a very short, wide viewport (roughly 320–400px tall), where the fixed parts alone can exceed the budget and `overflow: hidden` clips the controls. Degrade to a scroll-screen instead: `@media (max-height: 500px) { .app { height: auto; min-height: 100dvh; overflow: visible; } }`. In landscape the fit-screen degrades to a scroll-screen; do not add a separate landscape design unless the user asks.

## Verification

- Recompute the height budget from the final CSS and state it in the report (fixed total + absorber floor vs expected viewport).
- **State-geometry diff**: for every interactive element, list its states and check the state's rules against the base rules. If any box metric (border-width, padding, margin, size, font-size, font-weight) differs between states, fix it before shipping — do not wait for the defect to be seen on a real device.
- A build passing proves nothing about fit; a screenshot on a real phone is the ground truth. Say plainly that fit is verified by budget math and still pending a visual check on-device.
- When a "doesn't quite fit" report comes in, treat it as a real defect: recheck the budget first (a fixed part grew) before touching anything else.
