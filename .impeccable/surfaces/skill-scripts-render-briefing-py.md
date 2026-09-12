---
version: 1
slug: "skill-scripts-render-briefing-py"
primary_target: "skill/scripts/render_briefing.py"
related_targets: ["skill/assets/index_template.html"]
---

Scope: the two files that generate the whole site — skill/scripts/render_briefing.py
(every daily edition page) and skill/assets/index_template.html (the archive home).
Visitor mode: Read. Audience: Ankit, on a phone, at dawn, skimming; occasionally a
person he forwards the link to. Job: know what matters in 30 seconds, with depth
available and never required.

## Direction contract

THESIS: A personal wire service, set with broadsheet care. The page refuses the
category default — a newspaper pastiche of serif headlines over cream with
coloured pills — by splitting labour between exactly two faces: monospace carries
every piece of machinery, serif carries every piece of reading. Nothing is a
rounded card with a shadow; hierarchy is rules and weight.

OWN-WORLD: Warm paper ground (#F7F4EA) on deep warm ink (#1A1815), antique gold
(#9A7828) for rules and the LEAD marker only. Mono (ui-monospace/SFMono/Menlo) for
datelines, timestamps, section labels, story numbers, ticker chips, CONTINUING tags,
READ MORE, edition and read-time meta. Serif (Georgia/Iowan Old Style) for the
nameplate, every headline, every sentence of body copy. Section accent survives as a
2px rule above the section and a thin rule over each card's kicker — never as a
filled pill. Recognisable with all content removed by: the centred nameplate between
two gold dateline rules, the double hairline close, and the mono/serif split.

STORY: The reader lands on a dateline, a nameplate, and a lead marker; reads eight
skim lines; then either stops, or walks eight numbered sections. They understand the
day, and they know which stories are continuations of yesterday's.

FIRST VIEWPORT: Slim ink brand bar (dL mark, THE DATE LINE in tracked mono, theme
toggle). Beneath, on paper: a centred mono dateline rail flanked by gold hairlines;
the nameplate "The Date Line" in large serif; a mono subtitle line reading
ANKIT'S MORNING BRIEFING · N STORIES · ~N MIN; a double hairline rule; the LEAD
marker with the day's single most distinctive headline in serif; the mono section
index separated by hairlines; then THE 30-SECOND SKIM with mono numerals against
serif sentences.

FORM: "The Dispatch" — fusion of the Wire and Broadsheet directions at the user's
instruction (Wire's structure, Broadsheet's elegance), masthead variant B (centred).
Candidate 2 and 4 of the grounded list, fused. Seed key 20609248.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish
review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
