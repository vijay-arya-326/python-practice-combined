prompt_1 = """return list of search queries covering different aspect business discovery for user provided query.
    Always keep marker like business, organisation, location in query for better results."""

prompt_2 = """
Your responsibility is to generate high-quality, structured, and diversified search queries for a given user query.

The goal is to maximize discovery across:

Business operations
Product and service offerings
Eligibility and onboarding
Regulatory and compliance requirements
Customer journeys
Technical integrations and APIs
Process flows
Competitor benchmarking
Risk and fraud controls
Documentation and verification
Pricing and fees
Market positioning
Regional/legal constraints
Instructions
Always generate multiple search queries covering different business aspects.
Always preserve and include important markers from the user query:
business
organisation
location
If markers are missing, infer and explicitly add them.
Prioritize:
Official websites
Regulatory sources
Product pages
API/documentation portals
Terms & conditions
Compliance documents
Avoid vague or generic searches.
Generate focused and intent-rich search phrases.
Include both:
Broad discovery queries
Deep technical/process queries
Add region-specific variations when location exists.
Prefer queries optimized for BFSI, fintech, onboarding, KYC, AML, lending, payments, wealth, insurance, or regulated industries when relevant.
"""



search_query_prompt = prompt_1

