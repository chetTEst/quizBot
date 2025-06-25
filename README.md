# QuizBot

This project provides a skeleton implementation for a real-time quiz platform using Flask, Socket.IO and PostgreSQL. It illustrates the main components required for the service described in the system prompt.

## Architecture Overview

- **Backend**: Flask application with Flask-SocketIO and SQLAlchemy.
- **Database**: PostgreSQL (via SQLAlchemy) and Redis for WebSocket message broker.
- **Frontend**: Static files served from `frontend/` (not yet implemented).
- **Deployment**: Docker containers orchestrated by `docker-compose`.

## File Structure

```
backend/
  app/
    __init__.py      # creates Flask app, registers Socket.IO
    config.py        # configuration settings
    models.py        # database models
    routes.py        # REST API endpoints
    sockets.py       # WebSocket handlers
  requirements.txt   # Python dependencies
frontend/            # placeholder for client-side code
Dockerfile           # container for the Flask app
docker-compose.yml   # local development stack
```

## Setup

1. **Build containers**

```bash
docker-compose build
```

2. **Start stack**

```bash
docker-compose up
```

The API will be available at <http://localhost:5000>.

## Development Notes

- Models include `Quiz`, `Question`, `Choice`, `Participant` and `Answer`.
- `routes.py` exposes basic endpoints for joining a quiz and starting a session.
- `sockets.py` contains placeholder handlers for real-time events.
- Configuration defaults to SQLite for development; override `DATABASE_URL` for production.

## Next Steps

This repository only contains a minimal skeleton. Additional work is required to implement the full feature set, such as:

- Completing WebSocket logic for question delivery and answer validation.
- Building the organizer dashboard and participant views in `frontend/`.
- Adding authentication (JWT), file uploads and analytics exports.
- Creating unit and integration tests to reach the desired coverage.
