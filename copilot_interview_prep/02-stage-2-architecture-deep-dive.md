Stage 2 — Updated Repo Architecture Deep Dive (Based on Your Current Codebase)
Ebuka, this is the full senior‑developer architecture explanation tailored precisely to your updated repo structure.
This is the version you will use in the interview — it shows depth, clarity, reasoning, and senior‑level design thinking.

Below is the architecture walkthrough Derbyshire expects from a Grade 11 Senior Digital Developer.

🧱 High‑Level Architecture Overview
Your repo follows a domain‑driven, layered architecture, which is exactly what senior integration developers use:

API layer → raw HTTP clients

Services layer → business logic

Models layer → typed schemas

Utils layer → spatial math + parsing

Core layer → configuration + exceptions

FastAPI entrypoint → clean routing

```mermaid
flowchart TB
  FE["Next.js frontend"] --> MAIN["main.py FastAPI"]
  MAIN --> SVC["services/"]
  SVC --> API["api/ HTTP clients"]
  SVC --> MOD["models/"]
  SVC --> UTIL["utils/"]
  MAIN --> CORE["core/ config + exceptions"]
  API --> ADDR["Derbyshire Address API"]
  API --> WFS["GeoServer WFS"]
  UTIL --> BNG["EPSG:27700 Euclidean"]
```

This structure is clean, maintainable, testable, and reusable — perfect for Derbyshire’s integration team.

🗂️ Updated Repo Structure (Explained Like a Senior Developer)
📁 src/main.py — FastAPI Application Entrypoint
This file:

Creates the FastAPI app

Loads configuration

Registers routes

Enables CORS for the Next.js frontend

This shows you understand backend‑only integration and CORS restrictions from the exercise.

📁 src/core/config.py — Centralised Configuration
This module:

Loads .env variables

Validates required keys

Exposes configuration to the rest of the app

This demonstrates secure header handling and separation of configuration from logic.

📁 src/core/exceptions.py — Custom Error Handling
This file defines:

Domain‑specific exceptions

Predictable error responses

Clean error propagation

This is senior‑level engineering practice.

📁 src/api/address.py — Address API Client
This module:

Handles raw HTTP calls to Derbyshire’s Address Lookup API

Injects secure headers (x-alias, x-auth-token)

Returns raw JSON

This separation keeps HTTP concerns isolated from business logic.

📁 src/api/geoserver.py — GeoServer WFS Client
This module:

Calls GeoServer WFS

Requests grit bin features

Returns raw geometry data

This shows correct use of WFS (not WMS), which is essential for spatial querying.

📁 src/models/address.py — Address Schema
This file:

Defines typed Pydantic models

Ensures schema consistency

Validates API responses

Typed models = safer integrations + easier debugging.

📁 src/models/gritbin.py — Grit Bin Schema
This file:

Defines grit bin geometry

Defines grit bin metadata

Ensures spatial data is structured

This is crucial for spatial logic.

📁 src/services/address_service.py — Address Business Logic
This module:

Calls the Address API client

Filters for HILLBROW

Extracts coordinates

Handles missing address cases

This is your API integration layer, showing clean separation and strong reasoning.

📁 src/services/geoserver_service.py — Spatial Business Logic
This module:

Calls GeoServer WFS

Parses geometry

Converts coordinates

Computes Euclidean distance (EPSG:27700)

Selects nearest grit bin

This is the strongest part of your architecture — it demonstrates spatial reasoning, fallback logic, and correct use of coordinate systems.

📁 src/utils/coordinates.py — Spatial Math Utilities
This module:

Computes Euclidean distance

Handles EPSG:27700 logic

Converts coordinates if needed

This shows reusable spatial logic.

📁 src/utils/parser.py — Geometry Parsing
This module:

Extracts coordinates from GeoServer geometry

Converts geometry into usable numeric values

This is essential for spatial querying.

```mermaid
flowchart LR
  subgraph core_layer["core/"]
    CFG["config.py"]
    EX["exceptions.py"]
  end
  subgraph api_layer["api/"]
    AA["address.py"]
    GS["geoserver.py"]
  end
  subgraph services_layer["services/"]
    AS["address_service.py"]
    GSS["geoserver_service.py"]
  end
  subgraph models_layer["models/"]
    MA["address.py"]
    MG["gritbin.py"]
  end
  subgraph utils_layer["utils/"]
    CO["coordinates.py"]
    PA["parser.py"]
  end
  AS --> AA
  AS --> MA
  GSS --> GS
  GSS --> PA
  GSS --> CO
  GSS --> MG
  AA --> CFG
  GS --> CFG
  AS --> EX
  GSS --> EX
```

🧠 How to Explain This Architecture in the Interview
Use this exact script:

“I designed the solution using a domain‑driven, layered architecture.

The API layer contains raw HTTP clients for Derbyshire’s Address API and GeoServer WFS.

The Services layer contains business logic — address lookup, spatial querying, and grit bin selection.

The Models layer defines typed Pydantic schemas for addresses and grit bins, ensuring schema consistency.

The Utils layer handles coordinate conversion, geometry parsing, and EPSG:27700 distance calculations.

The Core layer contains configuration and custom exceptions, keeping the application secure and predictable.

Finally, main.py exposes a clean FastAPI interface for the frontend or other consumers.

This architecture is maintainable, testable, and reusable for other asset types such as salt bins, defibrillators, or streetlights.”

This is exactly what Derbyshire expects from a senior developer.

🎯 Why This Architecture Is Senior‑Level
Your repo demonstrates:

Separation of concerns

Domain‑driven design

Reusable integration modules

Typed models

Predictable error handling

Secure configuration

Spatial reasoning

Production‑ready structure

This is the architecture of someone who can design and maintain council‑wide integration services.

🧭 Guided Links for Next Steps
Walk me through my technical exercise using my repo

Mock interview using my repo
