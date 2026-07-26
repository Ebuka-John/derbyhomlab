Stage 4 — Updated Mock Interview Using Your Current Repo (derbyhomlab)
Ebuka, this is the full senior‑developer mock interview, rewritten to match your updated repo structure and your Derbyshire technical exercise.
This is exactly how the real panel will question you — and how you should answer.

Every question is followed by a model senior‑level answer grounded in your repo’s architecture and logic.

⭐ SECTION 1 — Opening & Background
Panel Question 1 — “Tell us about yourself and why you applied for this role.”
“I’m an Integration and Automation Developer with strong experience delivering API‑driven integrations, workflow automation, and AI‑enabled services across NHS and enterprise environments.

The Senior Digital Developer role aligns directly with my strengths: API integration, automation, digital forms, and modern backend development.

My repo demonstrates a domain‑driven FastAPI architecture that integrates with Derbyshire’s Address API and GeoServer WFS. It shows API integration, spatial querying, secure configuration, typed models, reusable services, and robust error handling — exactly the skills required for this role.”

⭐ SECTION 2 — Technical Exercise Deep Dive
Panel Question 2 — “Walk us through your solution.”
“I broke the problem into two integration tasks:

1) Address Lookup — retrieve HILLBROW’s coordinates using Derbyshire’s Address API.
2) Spatial Querying — use GeoServer WFS to find the nearest grit bin within ~100m.

My updated repo uses a layered architecture:

The API layer (api/address.py, api/geoserver.py) handles raw HTTP calls.

The Services layer (services/address_service.py, services/geoserver_service.py) contains business logic.

The Models layer (models/address.py, models/gritbin.py) ensures typed, validated schemas.

The Utils layer (utils/parser.py, utils/coordinates.py) handles geometry parsing and EPSG:27700 distance calculations.

The Core layer (core/config.py, core/exceptions.py) manages configuration and predictable error handling.

This structure keeps the solution maintainable, testable, and reusable.”

⭐ SECTION 3 — API Integration
Panel Question 3 — “Explain your API integration approach.”
“I separated raw HTTP concerns from business logic.

The Address API client injects secure headers from .env and returns raw JSON.

The Address Service filters the list, finds HILLBROW, validates the schema using Pydantic models, and extracts coordinates.

This separation keeps the integration clean, testable, and reusable.”

⭐ SECTION 4 — Spatial Querying
Panel Question 4 — “How did you handle spatial querying?”
“I used GeoServer WFS because WFS returns geometry, which is required for spatial calculations.

The GeoServer API client retrieves grit bin features.

The GeoServer Service parses SP_GEOMETRY using a dedicated parser, converts coordinates if needed, and computes Euclidean distance using EPSG:27700.

This ensures accurate results within the 100m range.”

⭐ SECTION 5 — Architecture Decisions
Panel Question 5 — “Why did you structure your repo this way?”
“I used a domain‑driven, layered architecture:

API layer → raw HTTP clients

Services layer → business logic

Models layer → typed schemas

Utils layer → spatial math + parsing

Core layer → configuration + exceptions

Each layer has a single responsibility, making the solution maintainable, testable, and reusable for other asset types.”

⭐ SECTION 6 — Error Handling
Panel Question 6 — “Explain your error handling strategy.”
“I implemented predictable exceptions in the core layer.

Services raise meaningful errors — missing address, missing grit bin, API failure, schema mismatch.

The API layer returns structured responses.

This ensures clarity, reliability, and easier debugging.”

⭐ SECTION 7 — Research & Reasoning
Panel Question 7 — “How did you investigate the APIs?”
“I tested the Address API in Postman, explored GeoServer WFS documentation, validated coordinate systems, inspected geometry fields, and tested CQL filters.

I verified results manually using distance calculations.

This ensured my approach was correct even with limited documentation.”

⭐ SECTION 8 — Follow‑Up Discussion
Panel Question 8 — “How would you make this reusable for other asset types?”
“I would parameterise the GeoServer layer name and geometry field so the same spatial module can query salt bins, defibrillators, streetlights, or any other asset.”

Panel Question 9 — “How would you return the nearest five grit bins?”
“Instead of selecting the minimum distance, I would sort all bins by distance and return the top five.”

Panel Question 10 — “How would you process a large batch of addresses?”
“I would build a queue‑based worker that processes addresses asynchronously, using bulk GeoServer queries and caching.”

Panel Question 11 — “How would you test and monitor this in production?”
“Unit tests for services, integration tests for API calls, logging, metrics, and alerts via Azure Monitor or ELK.”

⭐ SECTION 9 — AI Usage
Panel Question 12 — “Did you use AI to build this?”
“I used AI tooling to accelerate boilerplate setup, but all architectural decisions, integration logic, spatial reasoning, and error handling were designed intentionally.

AI helped with speed; the engineering decisions came from me.”

⭐ SECTION 10 — Behavioural Questions (Mapped to Derbyshire Values)
Panel Question 13 — “Tell us about a time you solved a complex integration issue.”
“At NHS Supply Chain, I resolved a multi‑system identity provisioning failure across ServiceNow, Azure AD, and Intune.

I traced schema mismatches, corrected Graph API calls, and implemented validation logic that prevented future failures.

This improved onboarding reliability and reduced manual intervention.”

Panel Question 14 — “How do you work collaboratively?”
“I work closely with service owners and technical teams, translating requirements into solutions.

I mentor colleagues and share documentation to support team growth.”

Panel Question 15 — “How do you stay innovative?”
“I design AI‑enabled workflows, multi‑agent pipelines, and automation services that reduce manual effort and improve SLA compliance.”

⭐ SECTION 11 — Closing
Panel Question 16 — “Why should we hire you?”
“My repo demonstrates the exact skills this role requires: API integration, spatial querying, modular architecture, secure configuration, typed models, reusable services, and robust error handling.

I bring strong experience across NHS digital operations, enterprise automation, and AI‑enabled services.

I’m ready to contribute immediately to Derbyshire’s digital transformation goals.”
