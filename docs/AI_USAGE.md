# AI Usage

I used AI as a helper during the BARQ project. I used it to understand some technical issues, work through selected configuration changes, and help prepare parts of the project documentation.

## AI assistance

AI helped with the following:

- PostgreSQL and Redis connection settings.
- Removing PostgreSQL and Redis host port mappings.
- PostgreSQL named volume and data persistence configuration.
- Redis AOF persistence.
- Database and Redis connectivity investigation.
- Understanding persistent storage and container recreation.
- Database configuration and persistence troubleshooting.
- Creating the GitHub Actions workflow.
- Checking recovery after restarting the stopped application.
- Dockerfile/runtime configuration and running the application as a non-root user, together with my own work.
- Restart policies, resource limits, and health checks, together with my own work.
- Pinning container images by digest, together with my own work.

## My work

I personally worked on:

- Reading the BARQ requirements and starter project.
- Fixing the Flask health-check path and binding address.
- Fixing the duplicate application instance ID.
- Correcting NGINX port mapping and upstream configuration.
- Configuring environment variables and `.env.example`.
- Separating frontend and backend networks.
- Checking container status, health.
- Investigating NGINX connectivity and application health-check issues.
- Investigating network and port configuration.
- Running the project with Docker Compose.
- Running `validation.py` and `failure_test.py`.
- Stopping `app-01` and checking requests through NGINX.
- Checking whether `app-02` continued serving requests.
- Creating and verifying database backups.
- Restoring a backup into a separate test database.
- Checking that records survived application and PostgreSQL container recreation.
- Reviewing the GitHub Actions run and its workflow steps.

## Both (Me and AI)

- Log analysis: reviewing the supplied logs, counting HTTP status codes and malformed records, checking duplicate request IDs, and correlating access, application, and NGINX error logs. I performed the analysis with AI assistance.

## Verification

I ran the project and its validation tests, checked the results, and reviewed the CI run. AI assistance did not replace running the project or checking the results myself.

## Scope

This disclosure covers AI assistance for the BARQ assessment work described above. It does not claim that AI independently completed the project.
