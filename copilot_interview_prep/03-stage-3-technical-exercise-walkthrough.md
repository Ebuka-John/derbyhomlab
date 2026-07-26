Stage 3 — Updated Technical Exercise Walkthrough Using Your Current Repo (derbyhomlab)
Ebuka, this is the exact walkthrough you will deliver during the interview — fully aligned with your updated repo structure.
It explains your solution clearly, confidently, and at a senior‑developer level, using your real architecture and business logic.

This is the version that will impress Derbyshire’s panel.

🧭 1. Start With Your Senior‑Level Problem Breakdown
“I approached the exercise by breaking it into two integration problems:

1) Address Lookup — retrieve the coordinates for HILLBROW using Derbyshire’s Address API.
2) Spatial Querying — use GeoServer WFS to find the nearest grit bin within ~100m.

My repo implements this using a clean, domain‑driven FastAPI architecture.”

This shows structured thinking — exactly what they want.

🧩 2. Address Lookup Flow (Based on Your Updated Repo)
Your updated repo uses a three‑layer approach:

API Layer → src/api/address.py
Sends raw HTTP request

Injects secure headers from .env

Returns raw JSON

Service Layer → src/services/address_service.py
Filters address list

Finds the record whose title contains HILLBROW

Extracts coordinates

Raises custom exceptions if not found

Model Layer → src/models/address.py
Validates structure

Ensures consistent schema

How to explain this in the interview:
“I separated raw HTTP concerns from business logic.

The Address API client handles the request and headers, while the Address Service handles filtering, validation, and coordinate extraction.

This keeps the integration clean, testable, and reusable.”

🌍 3. GeoServer Spatial Query Flow (Based on Your Updated Repo)
Your repo correctly uses WFS, not WMS.

API Layer → src/api/geoserver.py
Calls GeoServer WFS

Requests grit bin features

Returns raw geometry

Service Layer → src/services/geoserver_service.py
Parses geometry using utils/parser.py

Converts coordinates if needed

Computes Euclidean distance using utils/coordinates.py

Selects nearest grit bin

Returns Title + distance

Model Layer → src/models/gritbin.py
Defines grit bin geometry

Defines grit bin metadata

How to explain this:
“I used GeoServer WFS because WFS returns geometry, which is required for spatial calculations.

I parse SP_GEOMETRY using a dedicated parser, convert coordinates if needed, and compute Euclidean distance using EPSG:27700.

This ensures accurate results within the 100m range.”

📐 4. Spatial Reasoning (EPSG:27700)
Your repo demonstrates:

Correct use of British National Grid

Planar distance (Euclidean)

Geometry extraction

Coordinate parsing

How to explain this:
“Because the grit bin layer uses EPSG:27700, I used Euclidean distance, which is appropriate for planar coordinate systems.

This avoids unnecessary complexity and ensures accuracy.”

🚨 5. Error Handling (Your Updated Repo Does This Very Well)
Your repo now has:

core/exceptions.py → custom exceptions

Defensive checks in services

Clean error propagation to FastAPI

How to explain this:
“I implemented predictable exceptions for all failure scenarios — missing address, missing grit bin, API failure, and schema mismatch.

This ensures clarity, reliability, and easier debugging.”

🧱 6. Architecture Decisions (Updated Repo = Strong Senior‑Level Design)
Your repo uses:

API layer → raw HTTP clients

Services layer → business logic

Models layer → typed schemas

Utils layer → spatial math + parsing

Core layer → configuration + exceptions

FastAPI entrypoint → clean routing

How to explain this:
“I designed the solution using a domain‑driven, layered architecture.

Each layer has a single responsibility, making the solution maintainable, testable, and reusable for other asset types.”

🎨 7. Frontend Flow (Next.js)
Your frontend:

Accepts postcode + address

Calls FastAPI backend

Displays grit bin Title + distance

Handles loading + errors

How to explain this:
“The frontend is intentionally simple — it demonstrates how a user would interact with the backend service.

It validates input, calls the backend, and displays results cleanly.”

🧪 8. Investigation Notes (You MUST Say This During the Interview)
Your repo reflects:

Testing Address API in Postman

Exploring GeoServer WFS

Checking CQL filter support

Inspecting geometry structure

Verifying EPSG:27700 coordinates

Trying DWITHIN

Falling back to manual distance

How to explain this:
“I investigated GeoServer’s capabilities using documentation and test queries.

I validated coordinate systems, tested CQL filters, inspected geometry fields, and verified results manually using distance calculations.”

🚀 9. Improvements (Your Updated Repo Supports This Easily)
Say this:

“With more time, I would add caching, retry logic, API Management, and containerisation.

I would also extend the spatial module to support multiple asset types and batch processing.”

🧭 10. Follow‑Up Discussion Answers (Based on Your Updated Repo)
Nearest 5 grit bins
“Sort by distance, return top 5.”

Reusable for other asset types
“Pass layer name + geometry field into the spatial service.”

Batch processing
“Use a queue‑based worker + bulk GeoServer queries.”

Monitoring
“Add logging, metrics, and alerts via Azure Monitor or ELK.”

🎯 You are now fully prepared for the technical exercise discussion.
Your updated repo demonstrates everything Derbyshire is assessing:

API integration

Spatial querying

Research

Reasoning

Architecture decisions

Error handling

You just need to explain it confidently using the scripts above.

Reply “next” to continue to Stage 4 — Updated Mock Interview Using Your Repo.
