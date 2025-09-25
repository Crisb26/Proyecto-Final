#!/usr/bin/env bash
set -euo pipefail

echo "Starting build-all (bash)"

# Try to detect JDK21 in common location
if [ -d "/usr/lib/jvm" ]; then
  : # keep for linux compatibility
fi

SKIPTESTS="-DskipTests"
if [ "${1:-}" = "--run-tests" ]; then
  SKIPTESTS=""
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

build_module() {
  MODPATH="$1"
  echo "\nBuilding $MODPATH"
  if [ -x "$MODPATH/mvnw" ]; then
    "$MODPATH/mvnw" $SKIPTESTS clean package
  else
    (cd "$MODPATH" && mvn $SKIPTESTS clean package)
  fi
}

build_module "$ROOT_DIR/backend/microservicio-dispositivos"
build_module "$ROOT_DIR/backend/microservicio-usuarios"

echo "\nBuild-all finished"
