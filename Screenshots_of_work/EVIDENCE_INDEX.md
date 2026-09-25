# Evidence Index

This index lists evidence collected during the BARQ DevOps assessment.

Screenshots document the investigation, implementation, testing, and CI workflow. Configuration screenshots may show earlier troubleshooting states, so they are identified as investigation evidence rather than final configuration.

## 1. Architecture

| Evidence | Description |
|---|---|
| `architecture.png` | BARQ architecture diagram showing the user request flow, NGINX, Flask instances, PostgreSQL, Redis, networks, and storage. |
| `architecture.drawio` | Editable source of the architecture diagram. |

## 2. Investigation and Troubleshooting

| Evidence | Description |
|---|---|
| `evidence/01-initial-configuration.png` | Initial Docker Compose configuration and service settings reviewed during investigation. |
| `evidence/02-nginx-configuration.png` | NGINX configuration, upstreams, and routing settings inspected during troubleshooting. |
| `evidence/03-healthcheck-failure.png` | Application healthcheck failures and unhealthy container state during troubleshooting. |
| `evidence/04-nginx-routing-investigation.png` | NGINX upstream and application connectivity investigation. |
| `evidence/05-log-analysis.png` | Commands and log output used to investigate access, application, and error logs. |
| `evidence/06-request-correlation.png` | Correlation of a request ID across access, application, and error logs. |

## 3. Application and Validation

| Evidence | Description |
|---|---|
| `evidence/07-compose-services.png` | Docker Compose service status after starting the application stack. |
| `evidence/08-application-endpoints.png` | Successful application responses through NGINX, including health, readiness, and application endpoints. |
| `evidence/09-load-balanced-instances.png` | Repeated requests showing responses from both Flask application instances. |
| `evidence/10-validation-results.png` | Validation script completed with 16 checks passed and 0 failed. |

## 4. Failure and Recovery

| Evidence | Description |
|---|---|
| `evidence/11-failure-recovery-test.png` | Failure test stopped app-01, sent 20 requests through NGINX, observed app-02 serving requests, and confirmed app-01 recovery. |

## 5. Database Backup, Restore, and Persistence

| Evidence | Description |
|---|---|
| `evidence/12-database-backup.png` | Database backup command and archive verification. |
| `evidence/13-database-restore.png` | Restore test using the backup archive. |
| `evidence/14-persistence-test.png` | Persistence test showing the test record remained available after container recreation. |

## 6. CI/CD

| Evidence | Description |
|---|---|
| `evidence/15-github-actions-success.png` | Successful GitHub Actions workflow run for the project. |

## Notes

- Screenshots showing failed or unhealthy states are included as troubleshooting evidence, not as proof of the final working state.
- Do not include screenshots containing passwords, tokens, or other secrets.
- The architecture image and editable diagram are stored in the repository root.
