"""Synthetic Person store + incoming candidates for the RL-427 dry demo.

Entirely fabricated. No real people, no Twenty data. Used only to demonstrate
resolver / merge / fuzzy-QA behaviour without touching the live workspace.
"""

from engine_identity import Person, Candidate


def sample_people():
    return [
        # exact match by linkedinUrl; email is MISSING (merge can fill it)
        Person(id="p-001", linkedin_url="https://www.linkedin.com/in/dana-okafor",
               email=None, name="Dana Okafor", company_name="Northwind Freight",
               last_enriched_at="2026-05-01T00:00:00Z", enrichment_source="apollo",
               lifecycle_stage="lead", active_campaign_membership_id="cm-77",
               sourced_at="2026-04-10T00:00:00Z"),
        # exact match by email; linkedinUrl present
        Person(id="p-002", linkedin_url="https://linkedin.com/in/marcoreyes",
               email="marco.reyes@coastallogistics.com", name="Marco Reyes",
               company_name="Coastal Logistics", last_enriched_at="2026-03-15T00:00:00Z",
               enrichment_source="clay", lifecycle_stage="lead",
               sourced_at="2026-02-01T00:00:00Z"),
        # fuzzy target: same human as a candidate, slightly different name/company text
        Person(id="p-003", linkedin_url=None, email=None, name="Priya Nair",
               company_name="Summit Supply Chain", lifecycle_stage="lead",
               sourced_at="2026-04-20T00:00:00Z"),
        # two records that are the SAME person split across channels
        Person(id="p-010", linkedin_url="https://www.linkedin.com/in/sven-larsson-logistics",
               email=None, name="Sven Larsson", company_name="Baltic Cargo",
               last_enriched_at="2026-04-01T00:00:00Z", enrichment_source="apollo",
               lifecycle_stage="lead", active_campaign_membership_id="cm-91",
               sourced_at="2026-03-01T00:00:00Z"),
        Person(id="p-011", linkedin_url=None, email="sven.larsson@balticcargo.se",
               name="Sven Larsson", company_name="Baltic Cargo AB",
               last_enriched_at="2026-05-20T00:00:00Z", enrichment_source="clay",
               lifecycle_stage="lead", sourced_at="2026-05-15T00:00:00Z"),
        # exact-key collision: two records accidentally share one email
        Person(id="p-020", linkedin_url=None, email="ops@dupe-co.com",
               name="Lena Vogt", company_name="Dupe Co",
               sourced_at="2026-01-01T00:00:00Z"),
        Person(id="p-021", linkedin_url=None, email="ops@dupe-co.com",
               name="Lena Vogt", company_name="Dupe Co",
               sourced_at="2026-01-02T00:00:00Z"),
    ]


def sample_candidates():
    return [
        # A: matches p-001 by linkedinUrl, supplies the MISSING email -> match + fill
        Candidate(source="clay", linkedin_url="http://linkedin.com/in/dana-okafor/",
                  email="dana.okafor@northwindfreight.com", name="Dana Okafor",
                  company_name="Northwind Freight", last_enriched_at="2026-06-10T00:00:00Z",
                  enrichment_source="clay", sourced_from="apollo"),
        # B: matches p-002 by email despite a messy linkedinUrl variant -> match
        Candidate(source="apollo", linkedin_url="https://www.linkedin.com/in/marcoreyes?utm=abc",
                  email="MARCO.REYES@coastallogistics.com", name="Marco Reyes",
                  company_name="Coastal Logistics Inc"),
        # C: net-new, no keys collide and no fuzzy hit -> no-match
        Candidate(source="apollo", linkedin_url="https://linkedin.com/in/quinn-alvarez",
                  email="quinn@brightport.io", name="Quinn Alvarez",
                  company_name="Brightport"),
        # D: no exact key, strong name+company match to p-003 -> fuzzy-candidate
        Candidate(source="apollo", linkedin_url=None, email=None, name="Priya  Nair",
                  company_name="Summit SupplyChain"),
        # E: cross-key conflict -> resolves to two different persons (p-010 vs p-011)
        Candidate(source="clay",
                  linkedin_url="https://www.linkedin.com/in/sven-larsson-logistics",
                  email="sven.larsson@balticcargo.se", name="Sven Larsson",
                  company_name="Baltic Cargo"),
        # F: exact-key collision on shared email -> collision
        Candidate(source="apollo", email="ops@dupe-co.com", name="Lena Vogt",
                  company_name="Dupe Co"),
    ]
