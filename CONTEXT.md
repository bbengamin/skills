# Paperclip Skills

This context defines the language for skills that operate a Paperclip company through the `paperclipai` CLI.

## Language

**Paperclip**:
The AI organisation orchestration system documented at `docs.paperclip.ing` and operated locally through the `paperclipai` CLI.
_Avoid_: Pepper Clip, pepper clip

**paperclipai**:
The command-line interface used to configure a Paperclip instance and operate its control plane resources such as companies, agents, issues, approvals, skills, activity, and dashboards.
_Avoid_: Paperclip CLI when referring to the executable name

**Local Operator Skill**:
A Codex skill that a human operator invokes locally to inspect, shape, or administer a Paperclip company through `paperclipai`.
_Avoid_: Paperclip company skill, agent-attached skill

**Paperclip Company Skill**:
A reusable instruction package installed in a Paperclip company's skill library and attached to Paperclip agents for use during their heartbeats.
_Avoid_: Local operator skill

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
An outcome statement in Paperclip that explains why work matters and anchors projects; goals are not worked directly by agents.
_Avoid_: Task, project, issue

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
The Paperclip planning structure for a body of work: goal, linked project, and parent issue with a `plan` document; the chain may be fully new, fully existing, or partially missing.
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
The explicit operator phase after triage where approved work may be assigned or checked out. Agent pickup is handled by Paperclip heartbeat policy after assignment.
_Avoid_: Implicit pickup during planning, manual cross-agent heartbeat invocation

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
The local operator skill that establishes shared Paperclip CLI context, docs, glossary, and operating conventions for the rest of the Paperclip Operator Skill Suite.
_Avoid_: setup-matt-pocock-skills

**Creator Growth**:
The workflow for using creator-led distribution and personal-brand content to generate trust, qualified conversations, market learning, and acquisition leverage.
_Avoid_: Digital twin when voice/video/avatar cloning is out of scope

**Creator Growth Operator Skill Suite**:
Local operator skills that turn creator-growth intent into Paperclip-native goals, creator projects, strategy parent issues, campaign parent issues, planned work items, and AFK-readiness decisions.
_Avoid_: Treating creator strategy as generic Paperclip administration

**Creator Strategy Artifact**:
A Paperclip-native strategy parent issue and plan document that captures creator/persona, time horizon, channels, audience, hypothesis, positioning, source material, success signals, constraints, and stop conditions.
_Avoid_: Chat-only content plan, local-only brand brief

**Creator Project**:
A Paperclip project for one creator or persona, such as `Creator ops: Ihor`, that groups creator goals, strategy periods, channel campaigns, and execution work.
_Avoid_: One project per short-lived channel campaign by default

**Creator Campaign**:
A channel-specific or focused content hypothesis represented as a Paperclip parent issue under a strategy period, such as `LinkedIn campaign: logistics hypothesis X`.
_Avoid_: Permanent channel bucket, full business experiment tracker

**creator-clarify**:
The local operator skill that runs a non-mutating grilling session to turn rough creator-growth intent into a creator, channel, time-period, and campaign clarification summary.
_Avoid_: content drafting skill

**creator-record-strategy**:
The local operator skill that records approved creator-growth intent into Paperclip goals, a creator project, strategy parent issues, campaign parent issues, or plan documents, one missing layer at a time.
_Avoid_: creating an entire creator hierarchy without approval

**creator-plan-work**:
The local operator skill that decomposes a creator strategy or campaign artifact into one level of backlog, unassigned Paperclip work items.
_Avoid_: making creator work startable during planning

**creator-triage**:
The local operator skill that classifies planned creator work for AFK readiness before delegation to Paperclip agent execution.
_Avoid_: verification of completed creator outputs
