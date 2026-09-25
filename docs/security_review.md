# Security Review

This document records the security points I reviewed during the BARQ project and the changes made.

## 1. Exposed ports

**What I checked:** Which services were accessible through host ports.

**What I changed:** I removed the host port mappings for PostgreSQL and Redis. NGINX is the main service exposed to the host.

**Why:** The database and cache do not need to be accessed directly from outside the Docker environment.

## 2. Docker networks

**What I checked:** Which services could communicate with each other.

**What I changed:** I separated the frontend and backend networks and kept the backend network internal.

**Why:** This limits unnecessary access between services.

## 3. Application runtime user

**What I checked:** Which user the application runs as inside its container.

**What I changed:** I worked on the Dockerfile/runtime configuration so the application runs as a non-root user.

**Why:** Running as a non-root user reduces the permissions available to the application process.

## 4. Credentials and environment variables

**What I checked:** Where database and Redis connection settings were stored.

**What I changed:** I used environment variables and a local `.env` file, and added `.env.example` for the required settings.

**Why:** Actual local credentials should not be stored in the committed project files.

**Limitation:** A local `.env` file is not a complete secrets-management solution. Production deployments should use an appropriate secret store.

## 5. Container images

**What I checked:** How container images were referenced.

**What I changed:** I pinned selected images by digest.

**Why:** This makes the exact image content used by the project more consistent.

**Limitation:** Images still need to be reviewed and updated when security fixes become available.

## 6. Resource limits

**What I checked:** Whether containers had CPU and memory limits.

**What I changed:** I configured resource limits for the services.

**Why:** This helps prevent a container from using an unrestricted amount of host resources.

## 7. Restart policies and health checks

**What I checked:** How services behave when they stop or become unhealthy.

**What I changed:** I configured restart policies and health checks for the relevant services.

**Why:** These settings help the environment detect service problems and restart stopped containers.

**Limitation:** Restart policies and health checks do not guarantee that the whole application remains available.

## 8. PostgreSQL data and backups

**What I checked:** Whether database data remained available after container recreation and whether backups could be restored.

**What I changed:** I configured persistent PostgreSQL storage and created backup and restore scripts.

**What I tested:** I checked that a database record remained after container recreation and tested restoring a backup into a separate database.

**Limitation:** A local volume and backup file do not provide complete disaster recovery. Backups should also be stored securely outside the host.

## 9. Redis persistence

**What I checked:** Redis persistence settings.

**What I changed:** I enabled Redis AOF persistence.

**Why:** This provides a persistence mechanism for Redis data.

**Limitation:** Redis persistence is not a replacement for a separate backup and recovery plan.

## 10. Availability

**What I checked:** What happens when one application instance stops.

**What I tested:** I stopped `app-01` and sent requests through NGINX to check whether `app-02` continued serving requests.

**Limitation:** The project runs on one host. NGINX, the host, or shared services can still become single points of failure.

## Summary

The project includes several security and reliability improvements, including network separation, reduced host port exposure, environment-based configuration, a non-root application runtime, resource limits, health checks, and persistent database storage.

These changes improve the assessment environment, but they do not make it a complete production-ready system.
