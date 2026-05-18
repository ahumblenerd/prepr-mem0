#!/usr/bin/env bash
# Apply every migrations/*.sql file in lexical order against the dev db.
# Replaced by Alembic in Step 3; raw SQL is fine while the schema is one file.

set -euo pipefail

cd "$(dirname "$0")/.."

shopt -s nullglob
files=(migrations/*.sql)
if [[ ${#files[@]} -eq 0 ]]; then
    echo "no migrations to apply"
    exit 0
fi

for f in "${files[@]}"; do
    echo "applying $f"
    docker compose exec -T db psql \
        -U prepr -d prepr \
        -v ON_ERROR_STOP=1 \
        -q -f - < "$f"
done

echo "migrations done"
