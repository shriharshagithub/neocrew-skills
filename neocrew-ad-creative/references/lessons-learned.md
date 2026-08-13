# Quality lessons learned

These were each hit and fixed during development of this pipeline. Check for
them proactively rather than re-discovering them the hard way.

## Bulk "download selected" silently drops files past the first

Chrome (and other browsers) treat a `<a download>` click triggered from a
`setTimeout` callback as *not* tied to a direct user gesture, and silently
block automatic multi-file downloads after the first one — no error, they
just don't happen. This was caught by actually testing the "select several,
download" flow end to end, not by reasoning about it: a 2-file test looked
fine, a 3-file test quietly dropped the middle file. `build_review.py`
sidesteps this entirely by bundling any multi-selection into a single
in-browser-built `.zip` (see the `buildZip`/`crc32` functions in its
template) instead of firing N separate downloads — a single-file selection
still downloads directly. If you ever modify the download logic, keep it to
one `download` trigger per click, or re-introduce this bug.

## Headline wrapping to 3 lines

The template's headline is 2 lines by design — a 3rd line produces an ugly
orphan word and unbalances the whole layout. Before rendering a batch, check
each headline's line lengths (split on the `<br>` you inserted). If a line
runs long, it may soft-wrap again inside the browser even though you only
put one `<br>` in — count actual rendered characters per line, not just
where you put the tag.

After rendering, build a small contact sheet (a grid of shrunk thumbnails —
`sips -Z 260` each PNG, lay them out in an HTML grid, screenshot it) and
scan it visually for any 3-line headlines before delivering. This catches
wraps in seconds instead of opening every image individually.

## Mojibake from missing charset

Any generated HTML — the ad template, the review page, a contact sheet —
needs `<meta charset="utf-8">` as the very first thing after `<html>`/`<head>`
(before `<title>`). Without it, em dashes, curly quotes, and other non-ASCII
characters render as garbled text (`â€"`, `Â°`) in some browser/screenshot
contexts. Both `template.html` and `build_review.py`'s output already have
this — if you hand-write a new HTML file for this pipeline, don't drop it.

## Double-embedding images

If a page needs the same image for both display and download/lightbox,
read it once (`img.src` in the DOM) rather than storing a second base64 copy
in a data attribute. This exact mistake doubled a 50-image review page from
14MB to 29MB — caught only by checking file size before publishing.

## Artifact size cap

Claude Artifacts cap out around 16MB. A batch of ~50 full-resolution
(1080×1350) images needs JPEG (not PNG) at quality ~70 to fit comfortably
with headroom for the page's own HTML/CSS/JS. `build_review.py` prints an
estimated size and warns if it's over budget — don't ignore that warning.

## The `.card` wrapper needs explicit sizing

`template.html`'s `.card` div has `width:1080px; height:1350px;
position:relative;`. If this ever gets refactored and that rule is dropped,
the bottom bar (which is `position:absolute; bottom:0`) detaches from the
card and floats at the bottom of whatever the card's natural (unsized)
height happens to be, leaving a dead gap of empty background below it. If a
render ever shows a gap between the bottom bar and the true canvas edge,
check this first.

## Gradients that fade to near-black at the edges read as "dull"

Not currently a live risk — the locked design uses a single fixed navy
gradient, not a variable palette — but if a future direction experiments
with color again: a radial glow over a base color that goes to near-black at
the corners looks moody and dim regardless of hue. Keep gradient stops
mid-to-bright throughout the frame if testing new colors is ever explicitly
requested.

## Don't drift the locked visual design

The visual design in `template.html` was arrived at after several rejected
rounds (an abstract SVG-diagram system, an 8-color palette system, and a
bot-illustration system were all tried and explicitly rejected in favor of
going back to the original mascot-photo-on-navy-gradient look). Treat the
current template as locked. If a change to colors, layout, fonts, or
spacing seems like a good idea, treat that as a new, explicit decision to
confirm — not something to explore proactively while generating copy
variants.
