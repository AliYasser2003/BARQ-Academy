#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="backups"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="${BACKUP_DIR}/barq_tasks_${TIMESTAMP}.dump"

mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"
umask 077

echo "Creating PostgreSQL backup..."

if ! docker compose exec -T postgres \
    pg_dump -U barq_app -d barq_tasks -Fc > "$BACKUP_FILE"; then
    rm -f "$BACKUP_FILE"
    echo "FAIL: PostgreSQL backup command failed." >&2
    exit 1
fi

if [[ ! -s "$BACKUP_FILE" ]]; then
    rm -f "$BACKUP_FILE"
    echo "FAIL: Backup file is empty." >&2
    exit 1
fi

if ! docker compose exec -T postgres \
    pg_restore --list < "$BACKUP_FILE" > /dev/null; then
    rm -f "$BACKUP_FILE"
    echo "FAIL: Backup archive could not be inspected." >&2
    exit 1
fi

echo "PASS: PostgreSQL backup created and archive verified."
echo "Backup file: $BACKUP_FILE"
ls -lh "$BACKUP_FILE"
