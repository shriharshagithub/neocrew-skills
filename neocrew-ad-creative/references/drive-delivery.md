# Delivering the automated daily batch via Google Drive

The automated daily cloud routine delivers into Google Drive instead of a
Claude Artifact, so Shri's team can check a folder each morning without
needing a claude.ai account. This only applies to the automated routine —
for a manual/interactive run (Shri asking in a session), the Artifact +
zip delivery in the main workflow is still the right call, since he's right
there to click the link.

## The parent folder

**Folder name:** `NeoCrew Daily Ad Creative`
**Folder ID:** `1eG_g3FW3KSZi34nHVzJwIlWls9KlK9Cj`
**Link:** https://drive.google.com/drive/folders/1eG_g3FW3KSZi34nHVzJwIlWls9KlK9Cj

This folder's sharing is set to "Anyone with the link — Viewer" (a one-time
manual step, done outside this pipeline — Drive's MCP connector has no
permission-setting tool, so this can't be automated, and shouldn't be
re-attempted). **Anything created inside it inherits that same sharing
automatically** — this is standard Drive behavior, not something this
pipeline needs to set per-file or per-subfolder. Do not try to set
permissions on the subfolders or files you create; just create them inside
the parent and the inheritance handles the rest.

## What to upload, and how

1. After rendering the day's batch (following the main SKILL.md workflow
   through step 7 — quality-check), create a new subfolder inside the
   parent, named with today's date: `YYYY-MM-DD` (e.g. `2026-08-14`). Use
   the `create_file` Drive tool with `mimeType:
   "application/vnd.google-apps.folder"` and `parentId:
   "1eG_g3FW3KSZi34nHVzJwIlWls9KlK9Cj"`.

2. Upload every full-resolution PNG from the render output into that new
   subfolder. For each file: read it, base64-encode it, and call
   `create_file` with `title` (the filename), `parentId` (the new
   subfolder's id), `base64Content`, `contentMimeType: "image/png"`, and
   `disableConversionToGoogleType: true` (keeps it a real downloadable PNG
   rather than anything Drive might otherwise convert it to).

   Drive's own folder view already gives a thumbnail grid, click-to-preview,
   and multi-select-download — that's the "browse and pick a winner"
   interface for this delivery path. Don't also try to upload the
   review.html review page; it's redundant here (Drive's own UI does that
   job) and would need JS execution Drive doesn't support anyway.

3. In your final summary (still write one — see SKILL.md step 10 / the
   "Automated daily runs" section), include the direct link to that day's
   new subfolder (`https://drive.google.com/drive/folders/<new_subfolder_id>`)
   alongside your pick of the strongest ad(s) and why.

## If the Drive tools aren't available

If `create_file` isn't in your available tools when an automated run
starts, don't silently fall back to something else or skip delivery —
say clearly in your summary that Drive delivery wasn't available this run,
and fall back to publishing a Claude Artifact + reporting its link instead,
so the day's batch isn't lost even if it's not where it's meant to be.
