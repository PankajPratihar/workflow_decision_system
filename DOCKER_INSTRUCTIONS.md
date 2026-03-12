# Docker Instructions

This platform supports running via Docker and Docker Compose for easy deployment and local development.

## Prerequisites
- Docker installed
- Docker Compose installed

## Running the System

1. **Build and Start the containers**:
   ```bash
   docker-compose up --build
   ```

2. **Access the Application**:
   The FastAPI application will be available at `http://localhost:3000`.

3. **Check Logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Stop the System**:
   ```bash
   docker-compose down
   ```

## Environment Variables
The following environment variables are configured in `docker-compose.yml`:
- `DATABASE_URL`: The connection string for the PostgreSQL database.
- `GEMINI_API_KEY`: Your Gemini API key (should be set in your host environment or a `.env` file).

## Database Persistence
The PostgreSQL data is persisted in a Docker volume named `postgres_data`. This ensures your workflow requests and audit logs are saved even if the containers are stopped or removed.
