# ADR-02: Selection of Python 3.11 and FastAPI for Application Backend

## 1. Status
**Approved** (2026-10-10)

## 2. Context
The application backend must expose high-performance REST APIs to mobile clients, validate complex geospatial and agronomic query parameters, and execute scientific equations (FAO-56 Penman-Monteith, root-zone water balance, multi-factor flood indices).

We considered:
1. *Node.js / Express or NestJS (TypeScript)*
2. *Go (Golang) with Gin/Echo*
3. *Python 3.11 with FastAPI (Selected)*

## 3. Decision
We adopt **Python 3.11** as the backend language runtime and **FastAPI** as the web framework, paired with **Pydantic v2** for validation and **SQLAlchemy 2.0 (asyncpg)** for database I/O.

## 4. Rationale & Trade-Offs
- **Zero Language Translation Gap**: Python is the lingua franca of Earth observation science, remote sensing, and hydrology. Validated scientific equations from Phase 4 (`packages/core`) run directly in production without the error-prone process of rewriting mathematical algorithms into JavaScript or Go.
- **Asynchronous Throughput**: FastAPI's ASGI architecture (`async`/`await` powered by Starlette and Uvicorn) provides I/O throughput comparable to Node.js and Go for database-backed REST queries.
- **High-Speed Rust Validation**: Pydantic v2 executes request parsing and physical range validation in compiled Rust, operating 5–15x faster than Python-based validators.
- **Automatic OpenAPI 3.0 Documentation**: FastAPI automatically generates interactive OpenAPI/Swagger specifications directly from Python type hints, ensuring strict frontend-backend contract synchronization.

## 5. Revisit Triggers
This decision will be revisited if:
- API CPU-bound serialization latency exceeds acceptable $P_{95}$ thresholds under heavy load, in which case performance-critical endpoints can be extracted into Go or Rust microservices.
