---
name: neocrew-ad-creative
description: Generates NeoCrew.ai static ad creative (1080x1350 portrait images for Meta/LinkedIn/Instagram) by rotating across five distinct pre-approved ad formats (bold text statement, big-stat, chat-thread, comparison table, receipt) with fresh quirky/playful copy each run — ready to select, download, and push live. Use this skill whenever Shri asks to generate ads, ad creative, ad variants, ad copy as images, marketing images, or campaign creative for NeoCrew — including requests like "make me some ads," "generate 20 ad variations," "I need creative for a LinkedIn campaign," or "give me some ad copy" when the deliverable should be an actual image, not just text. Also trigger if he references "the ad pipeline," "the creative pipeline," "today's batch," or wants to iterate on ad headlines/CTAs. This skill is also run on an automated daily schedule — see "Automated daily runs" below.

---

# NeoCrew Ad Creative

Renders NeoCrew ad images across five distinct visual formats (see "The ad
formats" below), batching however many headline/CTA variants are wanted,
then hands back a browsable, downloadable page plus a zip of
full-resolution files. This is a rendering and copy pipeline, not a
one-off design tool — your job on each run is to write good copy in the
approved voice, distribute it across formats and ICP niches, generate the
images, quality-check them, and package the result.

## Before you start

Read `references/copywriting-voice.md` — it has the approved tone, the
winning example headline and why it won, more approved examples to
tone-match against, and the facts to draw from. Don't write ad copy for this
skill without it; formal/corporate phrasing was explicitly tried and
rejected in favor of this voice.

Read `references/formats.md` — it documents each of the five formats, the
exact fields each one needs, and which angles/niches suit which format.
Don't guess at a format's field names; get them from this file.

Skim `references/lessons-learned.md` once — it's short, and every item in it
was a real bug hit while building this pipeline. Cheaper to read it now than
to re-discover any of them.

If this is the automated daily run (or anyone asks for Drive delivery
specifically), also read `references/drive-delivery.md` before you get to
delivery — the folder ID and upload procedure are there, not in this file.

## The ad formats

This skill deliberately rotates across **five different ad formats** —
`bold_statement`, `big_stat`, `chat_thread`, `comparison_table`, `receipt`
— rather than one locked template. An earlier version of this skill used a
single template (the NeoCrew mascot photo on a navy gradient); it worked,
but Shri explicitly asked for the *subject* to be different day to day, not
the same mascot image every time. Full detail on each format, its fields,
and which angle it suits is in `references/formats.md` — read it before
writing copy.

Every format still shares the same brand anchors (the NeoCrew logo, brand
blue `#2F6FEB`/`#5B8DFF`) so a mixed batch still reads as one campaign —
only the compositional subject changes. **Do not invent a sixth format or
change an existing format's layout/colors on your own initiative** — if
asked to, treat that as a new explicit decision (see "Iterating" below),
not something to explore proactively while just writing copy.

Each format has its own space constraints for how much text fits well —
`references/formats.md` and the format's own template give you a sense of
this (e.g. `chat_thread` messages need to read like real short texts, not
paragraphs). If unsure, keep it tight rather than verbose — every format in
this system rewards a short, punchy line over a long one.

## Workflow

1. **Scope the batch.** If Shri hasn't said how many ads or which ICP
   niche(s), ask — a batch of 4-6 to react to is very different from "give
   me 50." (If he's clearly extending or redoing a batch discussed earlier
   in the conversation, infer instead of re-asking. If this is the
   automated daily run, see "Automated daily runs" below instead of
   asking.) The four ICP niches to rotate across are in
   `references/copywriting-voice.md`; the five formats are in
   `references/formats.md`. Cover a real spread of both niche and format in
   anything bigger than a handful — don't let one niche or one format
   dominate just because it's easiest to write.

2. **Write the copy.** For each variant, pick a `format` from
   `references/formats.md` and produce that format's exact fields — match
   the voice in `references/copywriting-voice.md`. Save the variants as a
   JSON array to a working directory (see step 3), one object per ad, e.g.:
   ```json
   [
     {
       "label": "ad-01",
       "format": "bold_statement",
       "headline": "Your prototype called.<br>It wants a <span class=\"accent\">real backend</span>.",
       "subhead": "Auth, payments, a database that doesn't ghost you at 2am.",
       "cta": "Fix My Prototype"
     },
     {
       "label": "ad-02",
       "format": "chat_thread",
       "msg_user": "Just got quoted $85K for my MVP 😭",
       "msg_neo": "We'll build it for $2K. Want to see how?",
       "cta": "Show Me How"
     }
   ]
   ```

3. **Set up a working directory *inside this skill's own directory*** —
   e.g. `<skill_dir>/.runs/<short-label>/` — call it `$WORK` below. Put
   `variants.json` there. This has to live under the skill directory, not
   the scratchpad or `/tmp`: the file server in the next step is rooted at
   the skill directory so `/assets/...` resolves, and `render.js` requires
   the HTML files it's screenshotting to be reachable under that same root
   (it checks this and errors clearly if not). `.runs/` is gitignored-style
   scratch space — fine to leave old runs there or delete them after
   delivering.

4. **Start the local file server** (only if one isn't already running on
   the port you'll use — check first) rooted at the skill directory itself,
   so `/assets/icon.png` resolves:
   ```bash
   cd <this skill's directory> && python3 -m http.server 8934 &
   ```

5. **Generate the HTML files.** `generate.py` reads each variant's
   `"format"` field and templates it against the matching file in
   `formats/` automatically — no need to pick a template file yourself:
   ```bash
   python3 <skill_dir>/scripts/generate.py $WORK/variants.json $WORK/html
   ```

6. **Render to PNG.** Playwright needs to be installed once per machine —
   check first (`node -e "require('playwright')"` from
   `<skill_dir>/scripts/`), and if it's missing:
   ```bash
   cd <skill_dir>/scripts && npm install && npx playwright install chromium
   ```
   Then render (must be run so the html_dir resolves under the skill
   directory the server is rooted at — see the script's own note if this
   errors):
   ```bash
   node <skill_dir>/scripts/render.js $WORK/html $WORK/png 8934
   ```
   This renders in seconds even for large batches — no need to fall back to
   one-by-one browser-tool screenshots.

7. **Quality-check before delivering.** At minimum, spot-check one render
   per format used. For anything more than ~10 total, build a quick contact
   sheet (shrink each PNG with `sips -Z 260`, lay them in an HTML grid,
   screenshot that) and scan for headline overflow, off-center content, or
   anything else visibly off — this takes a few seconds and catches
   problems before Shri (or whoever's reviewing) sees them, which is the
   standard he's held this pipeline to.

8. **Build the review/download page and publish it:**
   ```bash
   python3 <skill_dir>/scripts/build_review.py $WORK/variants.json $WORK/png $WORK/review.html
   ```
   Publish `$WORK/review.html` as a Claude Artifact. It has per-card
   select checkboxes, a single-image download button, and a "download
   selected" bar that bundles multi-selections into one zip — this is the
   tool the daily reviewer (Shri or his creative lead) uses to browse
   everything and pick a winner. Don't regress to a plain gallery.

9. **Zip the full-resolution PNGs** (`$WORK/png/*.png`) and deliver
   alongside the Artifact link, for a one-click bulk grab.

10. **In your summary**, don't just list what you built — say what you'd
    pick if you had to pick one, and why, the same way you would for any
    creative review. Judgment has repeatedly been asked for here, not just
    raw output.

## Automated daily runs

This skill runs on an automated schedule (a cloud routine, separate from
any local session) so a fresh batch is ready before Shri's team checks in
each morning. On an automated run, there's nobody to ask scoping questions
of — use these defaults instead of asking:

- ~12-15 variants, distributed across all four ICP niches and all five
  formats (don't repeat the exact same niche+format+headline combination
  from the day before — vary the specific copy even when the angle
  repeats).
- Run the full workflow above through step 7 (quality-check included — an
  unattended run is exactly when a headline-overflow bug would otherwise go
  unnoticed until someone's already looking at a broken ad).
- **Deliver via Google Drive, not a Claude Artifact** — read
  `references/drive-delivery.md` for the exact folder ID and upload
  procedure before delivering. The team checks a shared Drive folder each
  morning, not a claude.ai link. Still write a closing summary (same
  standard as any manual run: what you generated, the day's folder link,
  and a pick of the 1-2 strongest ads and why) — it just isn't the primary
  delivery mechanism for this path.
- Clean up `.runs/` after delivering so it doesn't accumulate across days.

## Iterating

If Shri reacts to a batch ("these are dull," "I want different X," "go
back to Y"), that's real signal — fix the actual problem (see
`references/lessons-learned.md` for the patterns already hit: muddy
gradients, a weak illustration, doubled image embeds, wrapped headlines,
one repeated visual subject) rather than just producing another
undifferentiated batch. If he asks to change the format system itself —
add a format, retire one, change a layout — that's a deliberate new
instruction: confirm what's changing, update the relevant file(s) in
`formats/` and `references/formats.md` to match, so the next run (including
automated ones) doesn't drift back to the old behavior.
