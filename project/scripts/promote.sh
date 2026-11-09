#!/usr/bin/env bash
set -euo pipefail
target="${1:-test}"
case "$target" in dev|test|prod) ;; *) echo "Use dev, test or prod" >&2; exit 2 ;; esac
cd "$(dirname "$0")/.."
databricks bundle validate -t "$target"
databricks bundle deploy -t "$target"
databricks bundle run -t "$target" performance_job
databricks bundle summary -t "$target"
