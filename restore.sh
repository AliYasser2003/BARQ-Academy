#!/usr/bin/env bash
set -euo pipefail

BACKUP_FILE="${1:-}"

if [[ -z "$BACKUP_FILE" ]]; then
    echo "Usage: ./restore.sh <backup-file>" >&2
    exit 2
fi

if [[ ! -s "$BACKUP_FILE" ]]; then
    echo "FAIL: Backup file is missing or empty: $BACKUP_FILE" >&2
    exit 1
fi

TEST_DB="barq_restore_test"

echo "Checking backup archive..."
docker compose exec -T postgres pg_restore --list < "$BACKUP_FILE" > /dev/null

echo "Preparing isolated test database..."
docker compose exec -T postgres \
    dropdb --if-exists -U barq_app "$TEST_DB"

docker compose exec -T postgres \
    createdb -U barq_app -O barq_app "$TEST_DB"

echo "Restoring into $TEST_DB..."
if ! docker compose exec -T postgres \
    pg_restore -U barq_app -d "$TEST_DB" --no-owner --no-privileges \
    < "$BACKUP_FILE"; then
    echo "FAIL: Restore command failed." >&2
    exit 1
fi

echo "Verifying restored database..."
docker compose exec -T postgres \
    psql -U barq_app -d "$TEST_DB" -v ON_ERROR_STOP=1 \
    -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

echo "PASS: Backup restored into isolated database: $TEST_DB"
echo "The original barq_tasks database was not modified."
