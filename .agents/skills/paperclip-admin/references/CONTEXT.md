# Paperclip Skills

This context defines the language for skills that operate a Paperclip company through the `paperclipai` CLI, Paperclip MCP tools, and API fallbacks.

## Language

**Paperclip**:
The AI organisation orchestration system documented at `docs.paperclip.ing` and operated locally through `paperclipai`, Paperclip MCP tools, and API fallbacks.
_Avoid_: Pepper Clip, pepper clip

**paperclipai**:
The command-line interface used to configure a Paperclip instance and operate its control plane resources such as companies, agents, issues, approvals, skills, activity, and dashboards.
_Avoid_: Paperclip CLI when referring to the executable name

**Paperclip MCP**:
The Model Context Protocol surface for operating Paperclip control-plane records from agent hosts, used as the first fallback when a `paperclipai` command is unavailable or too brittle for a skill workflow.
_Avoid_: Treating MCP as the local setup authority

**Local Operator Skill**:
A Codex skill that a human operator invokes locally to inspect, shape, or administer a Paperclip company through `paperclipai`.
_Avoid_: Paperclip company skill, agent-attached skill

**Paperclip Company Skill**:
A reusable instruction package installed in a Paperclip company's skill library and attached to Paperclip agents for use during their heartbeats.
_Avoid_: Local operator skill

**Skill Reference Bundle**:
The generated, self-contained reference files shipped inside one skill so selective installers and cloud imports retain the context that skill needs. Shared material is authored in canonical repository docs rather than edited inside individual bundles.
_Avoid_: Manually maintained reference copy, cross-skill runtime dependency

**Ralph Loop**:
An autonomous agent loop where the agent repeatedly reads a plan and progress state, chooses one next item, implements it, validates it, records progress, and commits the result.
_Avoid_: Multi-agent orchestration, continuous unattended coding without a bounded task source

**AFK Loop**:
A bounded autonomous work loop that can run without the human watching every iteration because the task source, progress tracking, validation, and stop conditions are explicit.
_Avoid_: Unbounded autonomy, unattended work without acceptance criteria

**Paperclip Source of Truth**:
The rule that goals, projects, issues, comments, approvals, activity, agent assignments, and skill attachments in Paperclip are the canonical operating state for AFK work.
_Avoid_: File-based progress as canonical state, duplicate local task ledgers

**AFK-Ready Work**:
Paperclip work that has enough goal context, boundaries, acceptance criteria, assignment, validation expectations, and stop conditions for an agent to execute without continuous human supervision.
_Avoid_: Vague task, exploratory prompt, open-ended delegation

**AFK Readiness Signal**:
The Paperclip-native representation that an issue is ready for autonomous execution: the issue is in `todo`, has sufficient brief and acceptance criteria, has no unresolved `blockedByIssueIds`, and has any required plan or board decision captured before assignment.
_Avoid_: Labels as the only readiness source, free-text blocked comments without blocker links

**Paperclip Operator Skill Suite**:
A set of local operator skills that help a human prepare, delegate, monitor, and refine AFK-ready work in Paperclip while using Paperclip as the source of truth.
_Avoid_: A single monolithic Paperclip skill, ad hoc prompts without shared structure

**Paperclip Operating Workflow**:
The operator workflow that moves from human intent to AFK execution: shape the goal, create a strategy artifact, plan projects and issues, check AFK readiness, delegate to agents, monitor heartbeats and activity, then triage outcomes.
_Avoid_: Ralph Loop as the full Paperclip workflow

**Strategy Artifact**:
A Paperclip-native record of board intent, such as a parent issue, project, or issue document, that captures the goal, constraints, success criteria, and operating assumptions before work is decomposed.
_Avoid_: Local-only PRD, chat-only plan

**Paperclip Goal**:
An outcome statement in Paperclip that explains why work matters and anchors projects; goals are not worked directly by agents. Goals use native `level`, `status`, optional `parentId`, and optional `ownerAgentId` fields.
_Avoid_: Task, project, issue

**Paperclip Goal Level**:
The native Paperclip goal layer: `company` for a top-level north star, `team` for durable team/domain/motion outcomes, `agent` for a goal owned by a specific agent, and `task` only for rare goal-like narrow outcomes.
_Avoid_: Encoding hierarchy only in goal titles

**Paperclip Project**:
A concrete deliverable container in Paperclip that links to goals and groups issues, workspaces, runtime configuration, and project budget.
_Avoid_: Goal, strategy artifact by itself

**Parent Issue**:
An issue that represents a larger body of work and owns child implementation issues; when paired with a `plan` document, it can hold the strategy artifact for that body of work.
_Avoid_: Project, goal

**paperclip-clarify**:
The local operator skill that runs a grilling session to turn fuzzy intent into a clear goal, constraints, success criteria, risks, autonomy level, and open questions.
_Avoid_: paperclip-shape

**Clarification Summary**:
A structured, non-mutating output from `paperclip-clarify` that captures the resolved intent and asks for confirmation before any Paperclip control-plane records are created or changed.
_Avoid_: Auto-created strategy, implicit Paperclip mutation

**paperclip-record-strategy**:
The local operator skill that records clarified intent into Paperclip as the strategy artifact.
_Avoid_: to-prd

**Planning Chain**:
The Paperclip planning structure for a body of work: goal tree, linked project, and parent issue with a `plan` document; the chain may be fully new, fully existing, or partially missing.
_Avoid_: PRD as a standalone local artifact, project-only strategy

**paperclip-plan-work**:
The local operator skill that decomposes a strategy artifact into one level of backlog, unassigned Paperclip issue structure. It may classify which children look ready for triage, but it must not make work startable.
_Avoid_: to-issues

**Recursive Issue Planning**:
The rule that `paperclip-plan-work` plans one child-issue level at a time, then treats any issue that is still too broad as a new parent issue for a later planning pass.
_Avoid_: Fully expanded multi-level issue trees, horizontal issue dumps

**Too-Broad Issue**:
A Paperclip issue that is useful as a planning parent but not yet AFK-ready; the operator must explicitly approve creating it and can later run `paperclip-plan-work` on it to create child issues.
_Avoid_: Assigning broad placeholders to execution agents as if they were ready

**Planning Parent Issue**:
A too-broad issue created intentionally as the parent for a future recursive planning pass; after creation, the operator is asked whether to run `paperclip-plan-work` again for its child issues.
_Avoid_: Execution-ready issue, unplanned placeholder with no next planning prompt

**paperclip-triage**:
The local operator skill that classifies existing Paperclip issues and decides whether each one is AFK-ready, blocked, missing information, human-needed, ready to revise, ready to cancel, or done.
_Avoid_: ready-check as a separate skill

**Delegation**:
The explicit operator phase after triage where the operator prepares the complete issue handoff and review policy while unassigned, verifies quiescence, then assigns the executor exactly once. Assignment creates the pickup wake; queued or running execution is observed read-only.
_Avoid_: Implicit pickup during planning, environment overrides without operator intent, manual heartbeat/resume, comments after dispatch, duplicate assignment wakes, interrupt/unassign/reassign before retries settle

**Operator Approval Boundary**:
The rule that local operator skills report proposed Paperclip mutations first and only create or update control-plane records after the human operator approves.
_Avoid_: Silent mutation, implicit lifecycle changes

**paperclip-monitor**:
The local operator skill that inspects active Paperclip execution across agents, heartbeats, activity, approvals, costs, and blocked work.
_Avoid_: triage when referring to runtime observation

**Read-Only Monitoring**:
The rule that `paperclip-monitor` can inspect Paperclip dashboard, activity, agents, issues, approvals, costs, and blocked work without confirmation, but must ask before any mutation.
_Avoid_: Automatic retry, automatic approval resolution, automatic reassignment

**paperclip-admin**:
The local operator skill for ad hoc Paperclip administration, including narrow reads, minor approved control-plane changes, existing-agent administration, and company skill-library maintenance.
_Avoid_: Using planning, triage, or monitoring skills for one-off administration just because they can inspect nearby records

**paperclip-create-agent**:
The local operator skill for creating or hiring a new Paperclip agent through the native governance-aware workflow, including config discovery, org convention review, draft instructions, approval handling, creation, verification, and local CLI setup.
_Avoid_: Treating new-agent creation as a minor admin update

**Agent Provisioning**:
The approved Paperclip create-agent operation of creating or hiring a configured AI worker with role, manager, adapter, budget, heartbeat policy, instructions bundle, and attached company skills.
_Avoid_: Treating agent creation as issue planning, implicit delegation, or an unapproved side effect

**paperclip-setup**:
The local operator skill that establishes shared Paperclip CLI context, project-local or explicitly global Paperclip MCP configuration, docs, glossary, and operating conventions for the rest of the Paperclip Operator Skill Suite.
_Avoid_: setup-matt-pocock-skills

**Growth Strategy**:
The shared acquisition strategy layer that aligns inbound and outbound around the same ICP, wedge, proof, artifact ask, offer or CTA, success signals, validation expectations, and stop conditions.
_Avoid_: Treating inbound and outbound as unrelated strategy trees

**Growth Operator Skill Suite**:
Local operator skills that turn rough acquisition intent into Paperclip-native company/team goal trees, durable channel or motion projects, strategy parent issues, branch parent issues, and planned inbound or outbound work items.
_Avoid_: Generic Paperclip planning when the acquisition domain matters

**Durable Channel Or Motion Project**:
A Paperclip project for a stable acquisition surface, such as `Inbound: Ihor LinkedIn` or `Outbound: Operator walkthroughs`.
_Avoid_: Creating a project for every short-lived campaign, message sequence, content sprint, or lead list

**Growth Strategy Artifact**:
A Paperclip-native parent issue and plan document that captures acquisition outcome, goal structure, projects, time horizon, market, ICP, wedge, inbound role, outbound role, shared proof, artifact ask, CTA, success signals, constraints, validation, and stop conditions.
_Avoid_: Chat-only acquisition plan

**Inbound Branch**:
A strategy branch under a growth strategy artifact that plans trust-building, personal-brand, content-led, or channel-led acquisition work.
_Avoid_: Treating inbound as only content drafting

**Outbound Branch**:
A strategy branch under a growth strategy artifact that plans lead sourcing, enrichment, personalization, sequences, reply handling, warm intros, or operator walkthrough booking.
_Avoid_: Treating outbound as fully automated sending

**growth-clarify**:
The local operator skill that runs a non-mutating clarification session for shared acquisition strategy spanning inbound and outbound.
_Avoid_: Starting branch planning before shared inbound/outbound alignment exists

**growth-record-strategy**:
The local operator skill that records approved growth strategy into Paperclip company/team goal trees, durable channel or motion projects, parent issues, and plan documents.
_Avoid_: Creating inbound and outbound branches without a shared strategy artifact

**inbound-plan-work**:
The local operator skill that decomposes an approved growth strategy or inbound branch into one level of backlog, unassigned inbound/channel work items.
_Avoid_: Making inbound work startable during planning

**outbound-plan-work**:
The local operator skill that decomposes an approved growth strategy or outbound branch into one level of backlog, unassigned outbound work items.
_Avoid_: Sending messages, modifying CRM records, or making outbound work startable during planning

**inbound-triage**:
The local operator skill that classifies planned inbound, personal-brand, content-led, or channel-led growth work for AFK readiness before delegation.
_Avoid_: Publishing, scheduling, or approving ungrounded claims during triage

**Outbound Readiness Level**:
The level-aware readiness model used by `outbound-triage`: `O0 strategy`, `O1 asset-prep`, `O2 tool-work`, `O3 send-ready`, and `O4 reply-booking`.
_Avoid_: Treating a lead-list task and a send-launch task as the same risk level

**outbound-triage**:
The local operator skill that classifies planned outbound work for AFK readiness by readiness level before delegation.
_Avoid_: Sending outreach, launching campaigns, mutating CRM records, spending credits, or modifying external accounts during triage

**Outreach Operator Skill**:
A local operator skill that runs the outbound engine as an operator-driven pipeline over a lead list, beginning after triage and using Paperclip for run intent and Twenty for lead data.
_Avoid_: Treating outreach as autonomous sending, or as strategy/planning work

**Run Record**:
The operations-plane analog of a Strategy Artifact: one Paperclip artifact per run that captures campaign link, stage scope, ICP filters, Twenty segment pointer, tools, caps, suppression, QA gates, success signal, stop conditions, and a stage checklist. It is the durable state that lets an outreach run be dropped and resumed.
_Avoid_: Holding per-lead values in the Run Record, or treating a chat transcript as run state

**Checkpoint**:
A write to a Run Record's stage checklist and counts, made only after a step's completion criterion is met. It is both a save point an outreach run resumes from and a gate the run must pass before the next stage.
_Avoid_: Recording progress in a local file, or checkpointing before the stage's completion criterion is met

**Twenty Lead Ledger**:
The rule that Twenty owns lead, account, and contact records and their per-lead pipeline progress (sourcing provenance, identity status, enrichment status with provider, confidence, cost, eligibility, asset reference, outcome signal), while Paperclip owns run intent and signal. Engine skills `twenty-engine-sync` and `eligibility-gate` own the per-person verdict and CRM mutation.
_Avoid_: Duplicating per-lead progress into Paperclip or local ledgers

**outreach-clarify**:
The local operator skill that runs a non-mutating clarification session to pin the config of one concrete outreach run, producing an Outreach Run Spec.
_Avoid_: Re-clarifying strategy, planning issues, or mutating Paperclip or Twenty during clarification

**Outreach Run Spec**:
The non-mutating summary `outreach-clarify` produces: the resolved run config that `outreach-record-run` turns into a Run Record after operator approval.
_Avoid_: Treating the Run Spec as a committed Run Record before approval

**outreach-record-run**:
The local operator skill that materializes an approved Outreach Run Spec into a Paperclip Run Record and initializes its checkpoint, one run at a time, mutating Paperclip only.
_Avoid_: Running a stage, writing to Twenty, or starting work during record-run

**outreach-source**:
The operator stage runner that runs the source stage of a run: filtered sourcing (Apollo via composio, or import) into idempotent Twenty ingest through `twenty-engine-sync`, ending at a QA gate.
_Avoid_: Enriching or sending during source, or writing Twenty outside `twenty-engine-sync`

**outreach-resolve**:
The operator stage runner that runs the resolve stage of a run: identity match and golden-record merge over the sourced segment, delegating the per-person decision to `twenty-engine-sync` and routing fuzzy matches to human QA.
_Avoid_: Auto-merging fuzzy matches, or reimplementing identity rules

**outreach-enrich**:
The operator stage runner that runs the enrich stage as a per-lead Ralph worker: one lead per invocation through a cheapest-first provider waterfall, stopping when the run's required channel keys are filled, writing back through `twenty-engine-sync`.
_Avoid_: Batch-enriching in one pass, hardcoding a provider, or exceeding caps

**outreach-gate**:
The operator stage runner that runs the gate stage: applies the per-person `eligibility-gate` verdict and dedup, TTL, suppression, and routing over the segment via `twenty-engine-sync`.
_Avoid_: Moving a suppressed or no-consent person forward, or reimplementing the verdict

**outreach-assemble**:
The operator stage runner that runs the assemble stage: builds the omnichannel segment and grounded personalization assets for eligible, enriched leads, writing asset references through `twenty-engine-sync`.
_Avoid_: Ungrounded claims, or pushing/sending during assemble

**outreach-push**:
The operator stage runner that runs the push stage: creates the list in the wired sending tool (Instantly or Grinfi) and attaches it to a campaign. Activation is send-enabling and operator-gated.
_Avoid_: Auto-approving activation, or pushing suppressed or no-consent leads

**outreach-review**:
The operator stage runner that runs the review stage: pulls reply and campaign signal from the sending tools, reconciles outcomes to Twenty, and writes the operator's kill/continue signal back to the Paperclip campaign or strategy issue.
_Avoid_: Deciding kill/continue unilaterally, or sending replies without approval

**twenty-engine-sync**:
The shared engine skill that owns all Twenty reads and writes for the outbound pipeline: identity query, idempotent match-or-create, golden-record merge, fuzzy-match human-QA handoff, and suppression or routing writes. Additive and dry-run-first; used by both the operator `outreach-*` stage runners and Paperclip engine agents.
_Avoid_: Writing Twenty outside this skill, deleting or overwriting populated fields, sending, or spending credits

**eligibility-gate**:
The shared engine skill that returns the deterministic per-person verdict (reuse / re-enrich / source / suppress / skip) and routing for the outbound pipeline. Decision-only; `outreach-gate`, `outreach-enrich`, and Paperclip engine agents consult it before acting.
_Avoid_: Reimplementing the verdict in a caller, or writing Twenty from the gate
