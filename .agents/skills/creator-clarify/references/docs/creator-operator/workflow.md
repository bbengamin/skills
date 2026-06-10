# Creator Growth Operator Workflow

Creator Growth Operator Skills turn rough operator intent into Paperclip-native creator strategy, campaign structure, and AFK-ready work.

```text
intent -> clarify -> record strategy -> plan work -> triage -> AFK execution
```

## 1. Intent

Intent is the operator's input, not a Paperclip entity by itself. Examples:

- Plan next month's creator-led distribution for Ihor around AI logistics.
- Revise the Q4 creator strategy after the first month of signals.
- Test a LinkedIn campaign for a logistics MVP hypothesis.

## 2. Clarify

Use `creator-clarify` when the operator intent is fuzzy or high-level. It runs a non-mutating grilling session and ends with a structured clarification summary.

Resolve:

- creator/persona
- time horizon
- channels
- business or market hypothesis
- audience and ICP
- source material
- positioning and story
- scope and non-goals
- success signals
- constraints, risks, and stop conditions
- existing Paperclip goals, projects, or issues to connect to

## 3. Record Strategy

Use `creator-record-strategy` after the operator approves a clarification summary. It materializes only the next missing Paperclip layer.

Possible layers:

- strategic company goal
- related creator/persona team goal
- related expertise team goal
- creator project
- yearly strategy parent issue
- quarterly strategy parent issue
- monthly strategy parent issue
- channel or campaign parent issue
- plan document on a parent issue

Do not create a whole hierarchy in one step unless the operator explicitly approves that full proposal.

## 4. Plan Work

Use `creator-plan-work` on a selected strategy or campaign parent issue. It creates one child-issue level at a time.

Examples:

- Split a yearly strategy into quarterly planning parents.
- Split a quarterly strategy into monthly planning parents.
- Split a monthly strategy into channel/campaign parents.
- Split a LinkedIn campaign into research, angle, draft, revision, and signal-capture work items.

Planning creates `backlog`, unassigned structure. It must not assign agents, checkout work, or move issues to `todo`.

## 5. Triage

Use `creator-triage` to decide whether planned creator work is ready for AFK execution.

Creator work is ready only when an agent has enough creator, channel, strategy, source, output, acceptance, validation, and stop-condition context to act without continuous operator supervision.

## 6. AFK Execution

AFK execution is handled by Paperclip assignment and heartbeat policy after work is triaged and delegated. Creator Growth skills do not manually invoke another agent's heartbeat.

## Deferred

The following are out of scope for v1:

- `creator-verify`
- `creator-reflect`
- `creator-suggest-intent`
- `creator-schedule`
- `creator-publish`
- voice, video, avatar, or cloning workflows
- automatic posting or scheduling
- publishing platform selection
- analytics dashboard integrations
- CRM or sales pipeline ownership
- full business experiment tracking
- creating new creator-execution agents
