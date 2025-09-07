Created a multi-container app with Docker Compose.

Services running:

db → PostgreSQL 16, with a volume (db_data) for persistent storage.

api → Python app (FastAPI) served by uvicorn, connecting to the Postgres DB via service name db.

pgadmin → pgAdmin web UI for browsing and managing the Postgres database.

