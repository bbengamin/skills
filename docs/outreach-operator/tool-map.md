# Outreach Stage Tool Map

What each stage can do with the wired tools, and what must come from the operator. The tool surface is the `metamcp` sales aggregator. Verify exact names and schemas at run time; namespaces and counts drift.

Namespaces (as of this writing): `twenty` (CRM gateway), `grinfi` (LinkedIn + email outreach and CRM), `instantly` (email outreach), `Postiz` (social posting, inbound side), `composio` (connector gateway that reaches Apollo - `APOLLO_PEOPLE_SEARCH`, `APOLLO_PEOPLE_ENRICHMENT`, `APOLLO_BULK_PEOPLE_ENRICHMENT` - via `COMPOSIO_SEARCH_TOOLS` then `COMPOSIO_MULTI_EXECUTE_TOOL`). Clay is not in metamcp; it is a direct agent connection. Twenty writes still route through `twenty-engine-sync`, which uses `twenty__execute_tool`.

The operator gate is always required before external-account actions, credit or send spend, and any send-enabling step. The agent may read, dry-run, and stage freely.

## source

- Agent can: source from Apollo through composio (`composio__COMPOSIO_SEARCH_TOOLS` with `toolkits:["APOLLO"]`, then `composio__COMPOSIO_MULTI_EXECUTE_TOOL` over `APOLLO_PEOPLE_SEARCH` / `APOLLO_ORGANIZATION_SEARCH`); also pull from `grinfi__search_company_leads`, `grinfi__lookup_companies`; import a provided list with `grinfi__upload_csv`, `grinfi__import_leads_from_file`, or `instantly__create_lead`; ingest to Twenty via `twenty-engine-sync`.
- Operator required: provide the Apollo filter set; approve Apollo credit spend and a per-run volume cap; confirm the composio Apollo connection is authed (`APOLLO_GET_AUTH_STATUS`).

## resolve

- Agent can: query, match, merge, and route through `twenty-engine-sync` (`twenty__execute_tool`).
- Operator required: approve fuzzy-match merges surfaced to the human-QA queue.

## enrich

- Agent can: run the provider waterfall over free existing Twenty data, then `grinfi__enrich_leads` / `grinfi__enrich_companies`, `instantly__enrichment_enrich`, `instantly__verify_email`, Apollo enrichment via composio (`APOLLO_PEOPLE_ENRICHMENT`, `APOLLO_BULK_PEOPLE_ENRICHMENT`), and Clay through its direct agent connection as the paid fallback; check spend with `grinfi__get_enrichment_metrics`, `instantly__enrichment_count`; write results via `twenty-engine-sync`.
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

Apollo has no native namespace but is wired through `composio`: search with `COMPOSIO_SEARCH_TOOLS` (`toolkits:["APOLLO"]`), then run `APOLLO_*` tools via `COMPOSIO_MULTI_EXECUTE_TOOL`; confirm auth with `APOLLO_GET_AUTH_STATUS` before a run. Clay is not in metamcp; it is a direct agent connection supplied to the run, used as the paid enrichment fallback. For any other tool that is missing or unproven, route the decision to `growth-tooling-scout` before adopting it.
