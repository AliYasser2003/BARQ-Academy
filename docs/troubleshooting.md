# Troubleshooting Journal

This file records problems I faced while working on the BARQ assessment and other DevOps practice. It includes the symptoms, what I investigated, and the fixes or results that were confirmed.

## Part 1 — BARQ Assessment

### 1. Application health-check path did not match

**Problem:** The health check used `/healthz`, while the Flask application exposed `/health`.

**Investigation:** I checked the health-check configuration and the application endpoint.

**Fix:** I corrected the health-check path to match the Flask application.

**Result:** The health check could use the endpoint provided by the application.

### 2. Flask application was bound to localhost

**Problem:** The Flask application was configured to listen on `127.0.0.1`, which prevented access from other containers.

**Investigation:** I checked the application binding address and how the containers communicated.

**Fix:** I changed the application to listen on `0.0.0.0`.

**Result:** The application could accept connections through the container network.

### 3. Both application containers used the same instance ID

**Problem:** The two application containers had the same `INSTANCE_ID`.

**Investigation:** I checked the environment configuration for both instances.

**Fix:** I corrected the instance ID configuration so each application instance had its own ID.

**Result:** The instances could be distinguished during testing.

### 4. NGINX used the wrong listening and published ports

**Problem:** The Docker port mapping targeted port 81 in the NGINX container, while NGINX was listening on port 80.

**Investigation:** I compared the Compose port mapping with the NGINX listening port.

**Fix:** I corrected the port mapping to target the port NGINX actually used.

**Result:** The host port mapping matched the NGINX configuration.

### 5. NGINX upstream configuration used the wrong application ports

**Problem:** The NGINX upstream configuration pointed to the wrong application port.

**Investigation:** I checked the upstream addresses against the ports used by the Flask containers.

**Fix:** I corrected the upstream addresses and application ports.

**Result:** NGINX could route requests to the application containers.

### 6. PostgreSQL and Redis configuration problems

**Problem:** The database and cache connection settings needed to match the services configured in Docker Compose.

**Investigation:** I reviewed the connection settings and service configuration.

**AI assistance:** AI helped investigate and correct the PostgreSQL and Redis configuration.

**Fix:** The connection settings were moved to environment variables and configured for the Compose services.

**Result:** The application configuration matched the database and cache services.

### 7. Database and Redis were exposed through host ports

**Problem:** PostgreSQL and Redis had host port mappings even though they were intended for internal service communication.

**Investigation:** I reviewed which services needed to be reachable from the host.

**AI assistance:** AI helped with this configuration change.

**Fix:** I removed the PostgreSQL and Redis host port mappings.

**Result:** NGINX remained the main published entry point, while the database and cache were accessed through the Docker network.

### 8. PostgreSQL data needed to survive container recreation

**Problem:** Database data needed to remain available when the PostgreSQL container was recreated.

**Investigation:** I reviewed the database storage configuration and the difference between container storage and a named volume.

**AI assistance:** AI helped with the persistence configuration and investigation.

**Fix:** I configured a named volume for PostgreSQL data.

**Verification:** I created a record, recreated the application and PostgreSQL containers, and checked that the record remained available.

### 9. Redis persistence configuration

**Problem:** Redis persistence needed to be configured.

**AI assistance:** AI helped with the Redis AOF persistence configuration.

**Fix:** I enabled Redis AOF persistence.

**Result:** Redis had a persistence mechanism configured. This does not replace a separate backup and recovery plan.

### 10. Dockerfile and runtime configuration

**Problem:** The application runtime configuration needed hardening, including the user used to run the application.

**Work:** I worked with AI on the Dockerfile/runtime configuration and running the application as a non-root user.

**Result:** The runtime configuration was updated as part of the project changes.

### 11. Restart policies, resource limits, and health checks

**Problem:** The services needed appropriate restart behavior, resource limits, and health checks.

**Work:** I worked with AI on these configuration changes.

**Result:** Restart policies, CPU/memory limits, and relevant health checks were configured in Compose.

### 12. Container image references

**Problem:** The project needed more consistent references to the selected container images.

**Work:** I worked with AI on pinning selected images by digest.

**Result:** Selected images were referenced by digest in the Compose configuration.

### 13. Testing application instance failure

**Problem:** I needed to check what happened when one application instance stopped.

**Investigation and test:** I stopped `app-01` and sent requests through NGINX to check whether `app-02` continued serving requests.

**Result:** The failure test showed that `app-02` served requests while `app-01` was stopped. The test also recorded failed requests, so this did not prove uninterrupted availability.

### 14. Backup and restore testing

**Problem:** I needed to verify that a database backup could be created and restored.

**Work:** I created backup and restore scripts and tested restoring a backup into a separate test database.

**AI assistance:** AI helped with database persistence and backup/restore troubleshooting.

**Result:** The backup was verified and the restore test passed without replacing the original database.

---

## Part 2 — Broader DevOps Challenges

These challenges came from my DevOps practice outside the BARQ assessment. They are kept separate from the BARQ issues.

### 15. Docker Desktop and virtualization

**Problem:** Docker Desktop did not start because of virtualization or hypervisor-related settings.

**Investigation:** I checked the Docker Desktop startup problem and the virtualization environment.

**Result:** The exact final fix was not recorded in this journal.

### 16. Minikube Docker provider error

**Problem:** Minikube reported `PROVIDER_DOCKER_NOT_FOUND`.

**Investigation:** I checked the Minikube setup and its Docker provider requirement.

**Result:** The final resolution was not recorded here.

---

## Notes

- The BARQ issues and broader DevOps challenges are listed separately.
- I have not included unconfirmed failed attempts or invented root causes.
- Some earlier troubleshooting outcomes were not recorded in enough detail to claim a final resolution.
- The BARQ validation, failure test, backup/restore test, persistence test, and CI results are documented separately where appropriate.
