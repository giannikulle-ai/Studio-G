# Studio-G — working rules

## Specified wording ships verbatim

When a sketch, note or message gives an exact word, label, name or number, use it exactly as given. Do not expand it, soften it, or make it a sentence.

The empty state of *Lost in the Jungle* reads **On Course**, because the sketch says "if empty, say on course". It is those words and no others: not "Nothing lost", not a sentence about being on course. Title case applies to it, as it does everywhere.

If specified wording seems wrong, say so and ask. Do not improve it in passing.

## Title case

Title case globally, with no exceptions. Headings, labels, buttons, tool names, empty states. Standard title case, so short words inside a phrase stay lowercase: *Lost in the Jungle*, *Run a Batch Job*, *Where Are We?*, *On Course*.

Two things are not labels and stay as they are: sentences that carry content, such as a row's description or a log line, and anything in code or monospace.

Small labels are set in title case rather than being force-uppercased by CSS.

## Attachments: the transcript is the fallback

An image sent in chat is not always written to disk. Sometimes a path is given and the file is in the uploads folder; sometimes neither happens, and the same file sent three times still never arrives.

The session transcript holds every image either way, base64 encoded inside `~/.claude/projects/<project>/<session>.jsonl` as `{"type":"image","source":{"type":"base64","media_type":...,"data":...}}`. Parse the JSON lines, take the newest matching image, decode it. This works when the uploads folder does not.

Two things that cost three rounds when the icon came in:

- Searching the disk for `*.png` and `*.webp` cannot find bytes that live inside a `.jsonl`. File-type searches prove nothing about whether the data is available.
- One failed method is not an unavailable file. Ask where the session keeps everything it has received before telling the user to send it again.

Downscale before embedding: a browser canvas via Playwright does it without an image library. 160 px is plenty for an icon and costs about 10 KB.

## Words to avoid

- **"lands here", "landing spot", "where it lands."** Say what a thing is, or what it connects to.

## Do not invent content

Where a thing is not designed yet, draw it undefined rather than filling it in. The page has one way of saying so: a bare dashed outline, as on the eighth tool.

Lists of items, sample statuses and explanatory blurbs invented to make a mockup look finished are worse than an empty box, because they get mistaken for decisions. A placeholder panel is the same mistake one step removed: if a panel was not asked for, do not draw one and label it undefined. Draw nothing.

Buttons are decisions. Which actions a row offers, and what a tool opens, are the user's to pick.

Example data is the exception, and only where the shape is already agreed: the rows, the log and the load figures carry plausible example values so the layout can be judged.

## Where the console's rules live

`console/README.md` and `console/adapters/README.md` hold the design. Two that the mockup added, from the sketches:

- *Lost in the Jungle* holds anything stopped, failed, alerting, or finished and unread, whatever kind of thing it is.
- *Navigating* holds active sessions and the jobs they are waiting on. It is not a list of every connected device. Anything still running appears there and not in the log, so nothing shows up twice.
- The light is automatic, following the alert rule. The manual override lives in settings and nowhere else.
- The console page carries no build documentation. It sits behind the settings button.
- The block above the log is token spend: frontier tokens are what you pay for, so that figure leads.
- The three figures above the log are chosen by the user from a list, not fixed. A slot the user has not chosen reads Pick One with a dash, never a default I picked. Frontier is the one they chose.
- A row is its own box with the chevron inside it. The status marker sits outside the box, on the left, aligned to the row.
- Token spend layout is the user's to design.
- Every section head carries a 90 degree corner marker at its top left, from the sketch.
- The status marker on a row is a fixed square, top aligned with the row box, so shrinking a row never stretches it.
- Theme is Light, Dark or System, chosen in settings. System is the default.
- The app icon is the user's artwork, kept at `console/web/icon.webp` and embedded in the header at 160 px.
- Subsections are inset under their section head, starting where the head's text starts.
- The log filters are Everything, Frontier, You and Clients. Frontier selects by where the work ran; You and Clients select by who made the call.

## Documents

`docs/` mirrors the published artifacts so `tools/spec-check.py` can run over them in CI. Re-mirror in the same commit as a republish, and run the checker before pushing.
