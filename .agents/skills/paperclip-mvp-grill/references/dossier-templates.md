# GTM Dossier Templates

Use these headings and tables as the canonical Paperclip wiki format. Preserve stable hypothesis IDs across revisions. Omit instructional bracket text from the final dossier.

## Dossier

```markdown
# [Product Idea] — GTM Dossier

**Status:** Draft | Researching | Approved
**Version:**
**Last updated:**
**Paperclip goal:**
**Paperclip project:**
**Parent issue:**

## Core GTM Thesis

For **[beachhead customer]**, who struggles with **[observable costly pain]**, **[product]** provides **[outcome]**. They would pay because **[economic or operational value]**. Unlike **[current alternative]**, the product **[wedge]**.

Supporting claims: [H-001], [H-002], [H-003]

## 1. ICP One-Pager

### Beachhead Segment

[Specific description of the initial segment.]

**Qualifying attributes**

- Company or operating context:
- Role or team:
- Trigger:
- Existing tools or workflow:
- Relevant constraints:

**Explicit exclusions**

- [Who is not part of the initial segment]

### Primary User

- **Role:**
- **Job or workflow:**
- **Pain event:**
- **Frequency:**
- **Current workaround:**

### Economic Buyer

- **Role:**
- **Budget source:**
- **Purchase trigger:**
- **Approval process:**
- **Likely objections:**

### Pain and Consequences

[Describe the observable problem.]

- **Time impact:**
- **Financial impact:**
- **Operational or risk impact:**
- **Conditions that make it urgent:**

### Desired Outcome

- **Functional outcome:**
- **Economic outcome:**
- **Risk or emotional outcome:**
- **Expected time to value:**

### Reachability

- Where this segment can be found:
- Signals that identify a likely prospect:
- Communities, channels, or datasets:

### Evidence and Open Questions

- Supporting evidence:
- Open hypotheses: [H-001], [H-002]

## 2. Positioning

### Positioning Statement

For **[segment]** who **[pain and context]**, **[product]** is a **[category or frame]** that **[primary outcome]**. Unlike **[current alternative]**, it **[primary wedge]**.

### Positioning Components

- **Audience:**
- **Problem context:**
- **Category:**
- **Primary outcome:**
- **Current alternative:**
- **Primary wedge:**
- **Reason to believe:**

### Claim Boundaries

The positioning must not imply:

- [Unsupported claim]
- [Capability outside the initial scope]

### Supporting Claims

[H-001], [H-004], [H-006]

## 3. Pricing Hypothesis

### Initial Offer

- **Payer:**
- **Pricing model:**
- **Billing metric:**
- **Initial price or range:**
- **Included scope:**
- **Pilot or entry offer:**

### Pricing Rationale

The proposed price is anchored to:

- Current customer spending:
- Time or labour replaced:
- Financial value created:
- Risk or delay reduced:

### Expected Buying Logic

[Explain why the buyer would consider the price reasonable.]

### Key Assumptions

- [H-007] [Assumption]
- [H-008] [Assumption]

### Evidence

- [Source or observation]
- [Pricing benchmark]

## 4. Wedge

### Entry Use Case

[The narrow first use case where the product should win.]

### Current Alternative

[What the customer uses or does today.]

### Specific Advantage

[Why the product is materially better for this use case.]

### Mechanism

[What enables that advantage.]

### Switching Reason

[Why the advantage is large enough to change behaviour.]

### Time to Value

[How quickly the user experiences the benefit.]

### Why Now

[What has changed to make the wedge relevant now.]

### Initial Boundaries

The wedge does not currently claim:

- [Broader capability]
- [Unsupported differentiation]

### Related Claims

[H-003], [H-009]

## 5. Hypothesis and Risk Log

| ID | Claim | Domain | Type | Status | Evidence | If Wrong | Validation | Issue |
|---|---|---|---|---|---|---|---|---|
| H-001 | [One testable claim] | pain | hypothesis | untested | — | [Affected decision] | [Method] | — |

### Evidence References

#### E-001 — [Source name]

- **Source:** [Name and URL]
- **Accessed:** YYYY-MM-DD
- **Supports or contradicts:** [H-001]
- **Finding:** [Concise summary]
- **Limitations:** [What the source does not prove]

## 6. Validation Plan

[Insert one subsection per proposed validation issue using the template below.]

## 7. Revision History

| Version | Date | Change | Approved By |
|---|---|---|---|
| 1.0 | YYYY-MM-DD | Initial approved dossier | [Operator] |
```

## Validation issue

```markdown
### VAL-001 — [Bounded validation outcome]

**Source hypotheses:** [H-001], [H-002]

**Why it matters**

[State which artifact or downstream decision depends on these claims.]

**Method**

[Describe the bounded validation method.]

**Allowed sources**

- [Approved source or source type]

**Required evidence**

- [Evidence requirement]

**Deliverable**

[Expected output and where it must be recorded.]

**Acceptance criteria**

- [Observable completion condition]
- The dossier evidence references and affected hypothesis statuses are updated.

**Stop conditions**

- Paid data, purchasing, outreach, or external mutation is required.
- The approved scope cannot answer the claim.
- Evidence contradicts an approved core thesis and requires operator review.

**Blocked by:** None | [Issue ID]
**Paperclip status:** `backlog`
**Assignee:** None
**Paperclip issue:** Not created | [Issue link]
```

## Paperclip record preview

Before mutation, render the exact proposed objects in this order:

```markdown
## Proposed Paperclip Records

### Wiki Page

- **Title:** [Product Idea] — GTM Dossier
- **Content:** [Full final dossier]

### Team Goal

- **Title:** Validate [Product Idea] for GTM handoff
- **Parent:** [Existing goal ID and title]
- **Level:** `team`
- **Status:** [Proposed native status]
- **Description:** [Outcome-focused description]

### Project

- **Title:** [Product Idea] — MVP validation
- **Linked goal:** [Goal title or approved placeholder]
- **Description:** [Concrete validation deliverable]

### Parent Issue

- **Title:** Validate the core GTM hypotheses for [Product Idea]
- **Project:** [Project title]
- **Status:** `backlog`
- **Assignee:** None
- **Description:** [Summary and wiki link placeholder]

### Validation Issues

[Render every full validation issue.]

### Generated Fields

Paperclip IDs and links will be inserted after creation without changing approved meaning.
```
