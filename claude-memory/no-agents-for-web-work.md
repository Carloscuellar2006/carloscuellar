---
name: no-agents-for-web-work
description: "Never use Workflow or subagents for website design, copy, or code — Carlos has ruled it out"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9aeb542e-85af-49bf-99ba-b7680b5e9be5
  modified: 2026-09-20T23:10:57.573Z
---

Do not use the Workflow tool or spawn subagents for website design, page copy, or code building. Build it directly.

**Why:** Carlos said the output "comes out bad and spends all my credits." Both are true. A 13-agent workflow for his home page burned ~1.2M tokens and produced a text-heavy, essay-like page — roughly 1,500 words of body copy across a method section and six long FAQ answers — that reads like a document rather than a website. Delegating design and copy judgment to agents removed the taste from the loop; Claude then shipped it without pushing back on the length.

**How to apply:** Applies even when ultracode is on — this instruction is from the user and overrides the standing workflow default. Write the HTML/CSS/copy directly, keep it short, and show him something small before expanding it. Prefer one tight iteration he can react to over a comprehensive build. Also see [[decide-dont-survey]] — he wants a decision acted on, not a survey of options, and that does not mean farming the decision out to a panel of agents.
