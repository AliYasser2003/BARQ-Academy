k
# BARQ Systems — DevOps Internship Assessment

A containerized Flask application with two backend instances behind NGINX, PostgreSQL for persistent records, and Redis for counter operations.

## Current Architecture

- **NGINX:** public entry point at `http://127.0.0.1:8080`
- **Flask:** `app-01` and `app-02`
- **PostgreSQL:** backend-only service with a named data volume
- **Redis:** backend-only service with append-only persistence enabled
- **Networks:** NGINX connects to `frontend`; Flask connects to `frontend` and `backend`; PostgreSQL and Redis connect only to `backend`

Only NGINX publishes a host port. PostgreSQL and Redis are not directly exposed.

The current Compose configuration uses two Flask instances on port 8080. The final three-instance configuration on port 8090 must be demonstrated during the live video challenge before it is described as complete.

## Documentation

### Architecture
- [System Architecture](docs/architecture/architecture.png)
- [Architecture Source](docs/architecture/architecture.mmd)

### Assessment Phases
- [Phase 1 — Investigation](docs/phases/phase-1-investigation.md)
- [Phase 2 — Fixes](docs/phases/phase-2-fixes.md)
- [Phase 3 — Validation](docs/phases/phase-3-validation.md)


## Requirements

- Linux or WSL
- Docker Engine or Docker Desktop with Linux containers
- Docker Compose v2
- Git
- `curl`
- Python 3

## Configuration

Create your local environment file:

```bash
cp .env.example .env
nano .env
```

Set the required values using your own local lab credentials:

```dotenv
POSTGRES_PASSWORD=replace_with_a_local_password
DATABASE_URL=postgresql://barq_app:replace_with_a_local_password@postgres:5432/barq_tasks
REDIS_URL=redis://redis:6379/0
PUBLIC_PORT=8080
```

Use a URL-safe password or percent-encode special characters in the database URL. Keep `.env` private. Do not commit it or place credentials in source code or container images.

## Build and Start

From the repository root:

```bash
docker compose config --quiet
docker compose build
docker compose up -d
docker compose ps
```

Follow service logs:

```bash
docker compose logs --tail=100
docker compose logs -f nginx app-01 app-02
```

Check the public endpoint:

```bash
curl -i http://127.0.0.1:8080/
```

## API Checks

Check the application endpoints:

```bash
curl -i http://127.0.0.1:8080/health
curl -i http://127.0.0.1:8080/ready
curl -i http://127.0.0.1:8080/instance
curl -i http://127.0.0.1:8080/records
curl -i http://127.0.0.1:8080/counter
```

Create a PostgreSQL record:

```bash
curl -i -X POST http://127.0.0.1:8080/records \
  -H 'Content-Type: application/json' \
  -d '{"title":"BARQ test record"}'
```

Repeat `/instance` requests to observe which backend responds:

```bash
for i in {1..10}; do
  curl -s http://127.0.0.1:8080/instance
  echo
done
```

## Automated Validation

Run the validation script:

```bash
python3 validate.py
```

Review the reported PASS/FAIL results. The script returns a non-zero exit code if validation fails.

## Backend Failure and Recovery

Run the failure test:

```bash
python3 failure_test.py
```

The test stops one backend, sends requests through NGINX, measures successful and failed requests, restores the backend, and checks that it serves traffic again.

Review the output and record the observed availability and error count. Do not describe the service as having uninterrupted availability if requests failed during the test.

## PostgreSQL Backup and Restore

Create and verify a backup:

```bash
./backup.sh
```

The script creates a timestamped custom-format dump under `backups/`. Backups are local evidence and should not be committed.

Restore a selected backup into the isolated test database:

```bash
./restore.sh backups/your_backup_file.dump
```

Replace the example filename with the actual filename printed by `backup.sh`.

The restore script uses `barq_restore_test` and does not overwrite the original `barq_tasks` database. It leaves the test database in place after verification.

## Persistence Test

Create a record and note its ID:

```bash
curl -s -X POST http://127.0.0.1:8080/records \
  -H 'Content-Type: application/json' \
  -d '{"title":"Persistence verification"}'
```

Recreate the application containers while retaining the PostgreSQL volume:

```bash
docker compose up -d --force-recreate app-01 app-02
```

Then recreate PostgreSQL without deleting the volume:

```bash
docker compose up -d --force-recreate postgres
```

Check `/records` after each recreation and confirm the record remains present.

**Never use `docker compose down -v` during persistence testing.**

## GitHub Actions

The workflow is located at `.github/workflows/ci.yml` and runs on pushes and pull requests.

It checks the Compose configuration, builds the images, starts the services, waits for readiness, and runs `validate.py`. A validation failure causes the workflow to fail.

A green CI run confirms that the configured checks passed in the GitHub Actions environment. It does not prove production readiness, continuous availability, or completion of the live video challenge.

## Troubleshooting

Check service state and logs:

```bash
docker compose ps
docker compose logs --tail=100 nginx app-01 app-02
docker compose logs --tail=100 postgres redis
docker compose config --quiet
```

If a service is unhealthy, inspect its logs and configuration, address the cause, and then start the services again:

```bash
docker compose up -d
docker compose ps
```

## Stop Services Safely

Stop and remove the Compose containers and networks:

```bash
docker compose down
```

This command does not remove the named PostgreSQL volume. Do not add `-v` unless you intentionally want to delete the database volume and have confirmed that doing so is safe.

## Documentation and Evidence

- [Troubleshooting journal](troubleshooting.md)
- [Log analysis](log_analysis.md)
- [Technical decisions](decisions.md)
- [Security review](security_review.md)
- [AI usage](AI_USAGE.md)
- [Evidence index](docs/EVIDENCE_INDEX.md)
- Architecture deliverable: `architecture.png` or `architecture.pdf`
The architecture diagram and evidence index must reflect the final demonstrated setup. Do not claim the three-instance port-8090 configuration is complete until it has been demonstrated live.
