# Architecture Diagram Requirements

Create the required architecture diagram as `architecture.png` or `architecture.pdf` in the repository root.

## System to Show
Show the final three-instance system, with NGINX exposed on host port `8090`.

Include:
- Client / browser
- NGINX reverse proxy: host port `8090` → container port `80`
- Three Flask application instances: `app-01`, `app-02`, and `app-03`, each listening on port `8080`
- PostgreSQL on port `5432`
- Redis on port `6379`

## Diagram Details
Label:
- Request flow from client through NGINX to the Flask instances
- Frontend and backend networks, including which services connect to each network
- PostgreSQL named volume and its mount path
- Redis persistence using AOF
- Health/readiness checks for the application, PostgreSQL, and Redis
- Service ports and network connections

## Availability Notes
Identify remaining single points of failure:
- One NGINX instance
- One PostgreSQL instance
- One Redis instance
- The host running the containers

The diagram must represent the final three-instance design, not only the current two-instance setup.

This note does not replace the required architecture diagram.
