---
name: paperclip-mvp-grill
description: Turn a committed product idea into an evidence-aware GTM dossier and approved Paperclip planning records. Use when an operator has decided to pursue an idea and needs to clarify the pain, user and buyer, beachhead segment, pricing hypothesis, positioning, and wedge; run bounded public research on the riskiest claims; then create a Paperclip wiki page, validation goal, linked project, parent issue, and unassigned validation issues. Do not use to score the opportunity, decide whether to build, red-team the idea, or plan downstream development, marketing, or analytics execution.
---

# Paperclip MVP Grill

Structure a committed product idea into clean, traceable artifacts for downstream development, marketing, and analytics. Treat this as a structuring and validation-planning workflow, never a go/no-go decision system.

## Required reference

Read [references/dossier-templates.md](references/dossier-templates.md) completely before compiling artifacts or proposing Paperclip records. Use its Markdown headings and tables as the canonical output shape.

## Non-negotiable boundaries

- Do not produce an opportunity score, fatal-gate report, weighted framework, build verdict, or red-team case.
- Do not let research overrule the operator. Surface contradictions and request confirmation.
- Do not create development, marketing, analytics, or placeholder implementation work.
- Create only bounded validation issues derived from open hypotheses.
- Keep new validation issues unassigned in `backlog`. Do not delegate or start execution.
- Perform no Paperclip mutation before the operator approves the exact mutation preview.

## Working ledger

Maintain these lists during the session:

- **Established facts**: traceable observations or evidence.
- **Approved hypotheses**: operator-authored or operator-accepted working claims.
- **Open hypotheses**: claims still needing evidence.
- **Contradictions**: evidence or answers that cannot both be true.

Give every material claim a stable ID such as `H-001`. Keep claim type and evidence status separate:

- Type: `fact` or `hypothesis`.
- Status: `untested`, `weak-signal`, `supported`, `contradicted`, or `mixed`.

Accepting a recommendation does not turn it into a fact. Mark it as a hypothesis.

## Workflow

### 1. Resolve Paperclip context

Identify the target Paperclip company and an existing company or product-portfolio goal under which the idea-validation goal should sit. Inspect available context instead of asking when it is discoverable.

Plan this hierarchy:

```text
Existing company/product goal
└── Team goal: Validate [idea] for GTM handoff
    └── Project: [idea] — MVP validation
        └── Parent issue: Validate the core GTM hypotheses
            └── Unassigned backlog validation issues
```

If no suitable parent goal exists, stop and ask. Never silently create a new company-level goal.

### 2. Run the grill

Work through the blocks below in order. Ask one question at a time so the operator can answer precisely. Use two or three questions from each block, adapting to answers rather than reciting every prompt.

#### Idea frame

- What is the product in one plain sentence, without positioning language?
- What event or observation led you to commit to it?
- What must this dossier clarify for downstream skills?

#### Pain and evidence

- Describe the last real occasion when someone experienced this problem. What happened?
- What do they do today, including tools, people, and workarounds?
- What does the pain cost in time, money, risk, delay, or lost opportunity?

#### User, buyer, and purchase

- Who experiences the pain directly, and who controls the budget?
- What causes the buyer to start looking for a solution?
- Who can approve, block, influence, or abandon the purchase?

#### Beachhead segment

- Which narrow group experiences this pain most often or severely?
- Which shared attributes make the group identifiable and reachable?
- Who is explicitly outside the first segment?

#### Value and pricing

- What measurable improvement would justify paying?
- Which existing cost, tool, effort, or lost outcome anchors the price?
- Who pays, how would they prefer to pay, and what initial range is plausible?

#### Alternatives and wedge

- What would the customer use if this product did not exist?
- For which first use case is this materially better or easier?
- What makes that advantage difficult for the current alternative to match immediately?

#### Synthesis

- What is the strongest reason the current GTM sentence may be wrong?
- Which unresolved claims would most change the customer, pain, willingness to pay, or wedge?
- Does the completion sentence accurately represent the working thesis?

### 3. Push back on vague answers

Do not accept labels such as “SMBs,” “marketing teams,” “inefficient,” “expensive,” “easy,” or “better” without observable detail.

Push toward:

- a recent concrete example;
- the person and workflow involved;
- frequency and trigger;
- measurable or observable consequence;
- current alternative;
- explicit segment boundaries.

Example: replace “They waste a lot of time” with “Who performed which steps during the last occurrence, how long did they take, and what was delayed?”

### 4. Help when the operator does not know

For a required field:

1. Ask up to two sharper diagnostic questions grounded in behavior, alternatives, or economics.
2. If unresolved, offer one reasoned recommendation and no more than two plausible alternatives.
3. Ask the operator to accept, edit, or reject them.
4. Record an accepted recommendation as a hypothesis.

Do not proceed with a blank beachhead customer, pain, outcome, reason to pay, or wedge. Require an operator-approved provisional hypothesis for each.

### 5. Compile the draft dossier

Use the reference template to compile:

- the core GTM thesis;
- ICP one-pager;
- positioning statement;
- pricing hypothesis;
- wedge description;
- hypothesis and risk log.

The completion sentence must state who the product is for, the observable pain, the outcome, why they would pay, the current alternative, and the wedge. Link every material clause to fact or hypothesis IDs.

### 6. Checkpoint 1: approve artifacts and research

Show the complete draft plus the proposed research set. Select three claims by default and no more than five with explicit operator approval.

Choose claims that are both load-bearing and weakly evidenced, especially claims about:

- competitor pricing or features;
- G2, Capterra, or similar review patterns;
- pain discussions on Reddit, Hacker News, or other public social sources;
- rough pricing benchmarks.

Do not calculate a risk score. Explain the selection in plain language. Wait for approval before research.

### 7. Run bounded research

After approval, perform or delegate a read-only public research pass. Record URLs, access dates, concise findings, claim IDs, and limitations.

Research may update evidence and validation status. It must not silently rewrite an approved strategic choice. Flag contradictory or mixed evidence for the operator.

Stop before:

- paid data or purchases;
- account login where no existing authorized access is available;
- outreach or messages;
- changes to external systems;
- research beyond the approved claims.

If research tooling is unavailable, continue. Mark affected claims `untested`, say that the pass was skipped, and create appropriate validation issues.

### 8. Derive validation issues

Map every open hypothesis to exactly one proposed validation issue. A single issue may cover up to three hypotheses only when they share the same method, evidence source, and completion criteria. Split the issue when failure of one claim would leave the others unresolved.

Each issue must include source hypothesis IDs, why the claim matters, method, allowed sources, required evidence, deliverable, acceptance criteria, and stop conditions. Keep it bounded enough for later AFK triage.

### 9. Checkpoint 2: approve exact Paperclip preview

Show the exact proposed records before writing:

- final wiki title and full Markdown;
- team goal title, description, status, parent, and level;
- project title, description, and linked goal;
- parent issue title and description;
- every validation issue, including linked hypotheses, acceptance criteria, blockers, priority, `backlog` status, and null assignee.

State that generated IDs and links will be inserted without changing approved meaning. If the operator edits anything, revise the preview and ask again. Do not mutate until approval is explicit.

### 10. Write and verify

Use the available Paperclip operator interfaces. Prefer confirmed native or documented routes; use existing Paperclip wiki-management procedures for the wiki when available.

Write in dependency order and make the operation idempotent:

1. Re-check whether approved records already exist.
2. Create only missing records and update only explicitly approved fields.
3. Insert generated Paperclip IDs and links into the dossier.
4. Read every record back.
5. Verify hierarchy, goal linkage, issue parentage, `backlog` status, null assignees, hypothesis links, and wiki content.

If a write fails halfway, stop and report exactly what exists and what remains. On retry, reuse matching approved records and create only what is missing. Never create duplicates or continue blindly.

## Completion criteria

Complete only when:

- the operator has approved both checkpoints;
- all required dossier sections exist in canonical Markdown;
- every completion-sentence clause links to a fact or hypothesis;
- every open hypothesis maps to one proposed validation issue;
- all Paperclip records have been read back and verified;
- downstream skills can consume the dossier without reconstructing the core thesis.

End with links to the wiki page, goal, project, parent issue, and validation issues, plus a short list of any claims still `untested`, `mixed`, or `contradicted`.
