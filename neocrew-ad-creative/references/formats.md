# Ad formats

As of August 2026, this skill rotates across **five distinct ad formats**,
not one locked template. This was a deliberate pivot: the earlier
single-template approach (mascot photo on a navy gradient, used across
several rounds) worked, but the subject was always the same "Neo robots"
image — repeated daily, it stopped feeling fresh. These five formats give
genuinely different subjects and compositions each run, drawn from ad
patterns that actually perform in the wild (bold text-only statements, a
dominant stat, a chat-message screenshot, a comparison table, a receipt) —
not just recolored versions of the same layout.

Every format keeps the same brand anchors — the NeoCrew logo and the brand
blue (`#2F6FEB` / `#5B8DFF`) — so a day's mixed batch still reads as one
campaign, but the actual visual subject differs completely format to
format. **Rotate across all five in any batch bigger than a couple of ads**;
don't let one format dominate just because it's the easiest to write for.

Each variant in `variants.json` needs a `"format"` field naming one of the
five below, plus that format's specific fields. `generate.py` looks up the
right template automatically.

## `bold_statement`

White background, a single giant headline (up to ~4 lines) dominates the
canvas, minimal supporting copy, understated text-style CTA. No imagery —
pure typographic punch, closest to a native "meme-style" text ad.

Wrap one phrase in `<span class="accent">...</span>` inside the headline to
color it brand blue — use this for the specific concrete thing being sold
(a price, "real backend", etc.), not a random word.

```json
{
  "label": "ad-01",
  "format": "bold_statement",
  "headline": "Your prototype called.<br>It wants a <span class=\"accent\">real backend</span>.",
  "subhead": "Auth, payments, a database that doesn't ghost you at 2am.",
  "cta": "Fix My Prototype"
}
```

## `big_stat`

Dark navy background, one huge number/stat as the hero visual, a small
uppercase label under it, then a supporting headline and subhead, then the
standard light bottom bar with CTA. Best for anything backed by a real
number: the price, the percentage saved, the 300+ products count.

```json
{
  "label": "ad-02",
  "format": "big_stat",
  "stat": "90%",
  "stat_label": "cheaper than a typical agency",
  "headline": "Same output. A fraction of the cost.",
  "subhead": "300+ products shipped for AB InBev, HDFC, Emaar, Coca-Cola, and UCSF.",
  "bottom_tag": "Fixed price. No subscription.",
  "cta": "See Pricing"
}
```

## `chat_thread`

Mimics a real text-message screenshot: a gray "incoming" bubble (the
founder's pain point) and a blue "NeoCrew" reply bubble (the offer), styled
like iMessage. Exactly two messages — keep both short, the way a real text
actually reads. This is a strong format for the "vibe-coder hit a wall" and
"agency sticker shock" niches specifically, since it reads as a relatable
moment rather than an ad.

```json
{
  "label": "ad-03",
  "format": "chat_thread",
  "msg_user": "Just got quoted $85K for my MVP 😭",
  "msg_neo": "We'll build it for $2K. Production-ready. Want to see how?",
  "cta": "Show Me How"
}
```

## `comparison_table`

A clean two-column table (Typical Agency vs. NeoCrew) with four fixed rows
— Cost, Timeline, Who owns it, Approval process — X/check marked. The row
content is fixed brand fact, not something to vary; only the headline and
CTA change per generation. Best for the agency-quoted-operator niche and
any price- or trust-led angle.

```json
{
  "label": "ad-04",
  "format": "comparison_table",
  "headline": "The math your agency hoped you wouldn't do.",
  "bottom_tag": "Fixed price. No subscription.",
  "cta": "Get Started"
}
```

## `receipt`

A stylized itemized receipt (monospace type, dotted item leaders, a
crossed-out agency-price comparison note) — the five build stages each
marked "INCLUDED," building to a total. Strong for the price-led angle and
for the "here's exactly what you get" framing.

```json
{
  "label": "ad-05",
  "format": "receipt",
  "headline": "Here's what $2,000 actually gets you.",
  "total": "$2,000",
  "agency_total": "$85,000",
  "bottom_tag": "Ship your MVP — from $2K, one-time",
  "cta": "Get My Receipt"
}
```

## Choosing a format per variant

Match format to angle rather than picking arbitrarily:

- Price-led angle -> `receipt` or `big_stat` (with a price/percent stat)
- Proof-led angle -> `big_stat` (with the 300+ stat) or `comparison_table`
- Vibe-coder-wall / relatable-pain angle -> `chat_thread` or `bold_statement`
- Agency-quoted-operator angle -> `comparison_table` or `receipt`
- Trust / not-a-black-box angle -> `comparison_table` (approval-process row)
  or `bold_statement`

When generating a batch, distribute across formats roughly evenly rather
than defaulting to whichever is fastest to write copy for — the entire
point of having five is that the day's batch doesn't look or feel
repetitive.
