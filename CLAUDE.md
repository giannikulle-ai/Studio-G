# Studio-G — working rules

## Specified wording ships verbatim

When a sketch, note or message gives an exact word, label, name or number, use it exactly as given. Do not expand it, soften it, or make it a sentence.

The empty state of *Lost in the jungle* reads **On course**, because the sketch says "if empty, say on course". It is not "Nothing lost. We're on course."

If specified wording seems wrong, say so and ask. Do not improve it in passing.

## Title case

Headings, labels, buttons and tool names are Title Case. Standard title case, so short words inside a phrase stay lowercase: *Lost in the Jungle*, *Run a Batch Job*, *Where Are We?* Sentences in rows and log lines stay sentences. Small labels are set in title case rather than being force-uppercased by CSS.

The one string this does not touch is the empty state of *Lost in the Jungle*, which stays **On course** as specified.

## Words to avoid

- **"lands here", "landing spot", "where it lands."** Say what a thing is, or what it connects to.

## Where the console's rules live

`console/README.md` and `console/adapters/README.md` hold the design. Two that the mockup added, from the sketches:

- *Lost in the jungle* holds anything stopped, failed, alerting, or finished and unread, whatever kind of thing it is.
- *Navigating* holds active sessions and the jobs they are waiting on. It is not a list of every connected device. Anything still running appears there and not in the log, so nothing shows up twice.
- The light is automatic, following the alert rule. The manual override lives in settings and nowhere else.
- The console page carries no build documentation. It sits behind the settings button.
- The block above the log is token spend: frontier tokens are what you pay for, so that figure leads.
- The three figures above the log are chosen by the user from a list, not fixed.

## Documents

`docs/` mirrors the published artifacts so `tools/spec-check.py` can run over them in CI. Re-mirror in the same commit as a republish, and run the checker before pushing.
