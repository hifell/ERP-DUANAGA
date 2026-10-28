#!/usr/bin/env bash
# Render odoo.conf from template using environment variables.
# The official Odoo image has no env-var interpolation in odoo.conf, so the
# secrets live in .env and are substituted here at container start.
set -euo pipefail

TEMPLATE="${ODOO_CONF_TEMPLATE:-/opt/duanaga/odoo.conf.template}"
TARGET="${ODOO_CONF_TARGET:-/etc/odoo/odoo.conf}"

: "${ODOO_MASTER_PASSWD:?ODOO_MASTER_PASSWD is required}"
: "${ODOO_DB_PASSWORD:?ODOO_DB_PASSWORD is required}"

export ODOO_DB_HOST="${ODOO_DB_HOST:-db}"
export ODOO_DB_PORT="${ODOO_DB_PORT:-5432}"
export ODOO_DB_USER="${ODOO_DB_USER:-odoo}"
export ODOO_LOG_LEVEL="${ODOO_LOG_LEVEL:-info}"
export ODOO_WORKERS="${ODOO_WORKERS:-2}"
export ODOO_MAX_CRON_THREADS="${ODOO_MAX_CRON_THREADS:-1}"
export ODOO_PROXY_MODE="${ODOO_PROXY_MODE:-False}"

python3 - "$TEMPLATE" "$TARGET" <<'PY'
import os
import re
import sys

template_path, target_path = sys.argv[1], sys.argv[2]

with open(template_path) as fh:
    content = fh.read()


def substitute(match):
    key = match.group(1)
    if key not in os.environ:
        raise SystemExit(f"missing environment variable: {key}")
    return os.environ[key]


rendered = re.sub(r"\$\{([A-Z0-9_]+)\}", substitute, content)

with open(target_path, "w") as fh:
    fh.write(rendered)
PY

chmod 600 "$TARGET"

# Delegate to the official image entrypoint so its own setup still runs.
exec /entrypoint.sh "$@"
