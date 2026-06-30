# Outreach Stage Tool Map

What each stage can do with the wired tools, and what must come from the operator. Tool surfaces vary by MCP client. Verify exact names and schemas at run time; namespaces, prefixes, counts, and gateway choices drift.

Common surfaces include `twenty` (CRM gateway), `grinfi` (LinkedIn + email outreach and CRM), `instantly` (email outreach), `Postiz` (social posting, inbound side), direct Apollo MCP tools, and connector gateways such as Composio that reach Apollo through discovered `APOLLO_*` slugs. Clay may be a direct agent connection rather than part of the aggregator. Twenty writes still route through `twenty-engine-sync`; do not bypass the engine skill even if direct Twenty tools are visible.

The operator gate is always required before external-account actions, credit or send spend, and any send-enabling step. The agent may read, dry-run, and stage freely.

## source

- Agent can: discover and bind a source surface at run time. For Apollo, bind usage or credit status, people search, and people match/enrichment when revealed work emails are required; bind auth/status and organization/company search when the surface provides them and the run needs them. Accept either direct Apollo tools or a gateway pattern such as Composio discovery plus multi-execute over returned `APOLLO_*` slugs. Also discover Grinfi list/import capabilities and file import tools by schema before use. Ingest to Twenty via `twenty-engine-sync`, and bind the run segment as non-send-enabled state (for example a `DRAFT` Campaign plus run-label memberships).
- Operator required: provide the Apollo filter set; approve Apollo credit spend, organization searches that charge per request, enrichment, imports, persistent jobs, CRM writes, and the per-run volume cap.

## resolve

- Agent can: query, match, merge, and route through `twenty-engine-sync` using the discovered Twenty meta-tool pattern (`get_tool_catalog` -> `learn_tools` -> `execute_tool`). The callable prefix can vary by client, so bind the exact catalog, schema-learning, and execution tool names before use.
- Operator required: approve fuzzy-match merges surfaced to the human-QA queue.

## enrich

- Agent can: run the provider waterfall over free existing Twenty data, then discovered Grinfi or Instantly enrichment/verification tools, Apollo enrichment through direct Apollo MCP tools or gateway-returned `APOLLO_*` slugs, and Clay through its direct agent connection as the paid fallback; check spend with the provider's available metrics or credit-usage tool; write results via `twenty-engine-sync`.
- Operator required: approve enrichment credit spend, set per-lead and run-level caps, and provide the Clay connection.

## gate

- Agent can: get the per-person verdict from `eligibility-gate`; read suppression state via `grinfi__list_leads_blacklist`; apply suppression with `grinfi__add_to_leads_blacklist`, `instantly__blocklist_create`, and routing via `twenty-engine-sync`.
- Operator required: approve the suppression and routing policy.

## assemble

- Agent can: draft messages and variables with `grinfi__create_ai_template`, `grinfi__render_ai_template`, `grinfi__list_ai_variables`, `instantly__custom_prompt_templates_create`, `instantly__email_templates_list`; write asset references via `twenty-engine-sync`.
- Operator required: approve message content and grounding at the QA gate.

## push

- Agent can: build and stage the send. Instantly: `instantly__create_lead_list`, `instantly__create_campaign`, `instantly__add_leads_to_campaign_or_list_bulk`, `instantly__move_leads_to_campaign_or_list`. Grinfi: `grinfi__create_list`, `grinfi__leads_mass_action_by_filter`, `grinfi__add_contact_to_automation`. Record membership via `twenty-engine-sync`.
- Operator required: explicit approval of the send-enabling action - `instantly__activate_campaign` or `grinfi__start_automation` - which begins automatic sending. Suppression and consent must be verified first; caps must hold.

## review

- Agent can: pull signal with `instantly__get_campaign_analytics`, `instantly__get_daily_campaign_analytics`, `grinfi__get_outreach_metrics`, `grinfi__get_dashboard`, `grinfi__list_outbound_log`, `grinfi__get_unread_conversations`; read replies via `instantly__list_emails`, `grinfi__list_linkedin_messages`.
- Operator required: the kill/continue decision; approval before any reply send (`instantly__reply_to_email`, `grinfi__send_email`, `grinfi__send_linkedin_message`).

## Tool Access Notes

Apollo may appear as direct MCP tools or through a gateway. Do not hard-code prefixes such as `composio__`, `mcp__metamcp`, `apollo__`, or client-specific spellings. First search the available tools for Apollo source capabilities, inspect complete schemas, and bind exact callable names. In one observed client, direct Apollo people search and enrichment were exposed as tools named like `Appolo_apollo_mixed_people_api_search`, `Appolo_apollo_people_bulk_match`, and `Appolo_apollo_usage_stats_credit_usage_stats`, while Composio exposed canonical slugs through a separate discovery and multi-execute pair. Either is valid if it exposes the needed schema and connection or credit guidance.

For a Composio-style gateway, call the gateway's discovery tool first, require an active Apollo connection, and use only returned `APOLLO_*` slugs and schemas. Typical source slugs are `APOLLO_GET_AUTH_STATUS`, `APOLLO_VIEW_API_USAGE_STATS`, `APOLLO_ORGANIZATION_SEARCH`, and `APOLLO_PEOPLE_SEARCH`. Never invent `APOLLO_*` slugs or argument fields.

If `twenty-engine-sync` is unavailable in the current client, stop before CRM ingest, resolve, gate, assemble, or push writes. Direct CRM tools may be useful for read-only reconnaissance, but they are not a substitute for the engine skill's idempotent match-or-create, provenance, and checkpoint semantics unless the operator explicitly approves degraded mode.

Clay is not guaranteed to be in the aggregator; it may be a direct agent connection supplied to the run, used as the paid enrichment fallback. For any other tool that is missing or unproven, route the decision to `growth-tooling-scout` before adopting it.
