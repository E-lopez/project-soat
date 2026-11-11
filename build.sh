#!/usr/bin/env bash
set -o errexit

echo "======= PHASE 1: Installing Python Requirements ======="
pip install --upgrade pip
pip install -r api/requirements.txt

echo "======= PHASE 2: Compiling Frontend Distribution ======="
cd ui
npx pnpm install --frozen-lockfile --config.onlyBuiltDependencies=esbuild
npx pnpm build
cd ..

if [ ! -d "ui/dist" ] || [ -z "$(ls -A ui/dist)" ]; then
  echo "ERROR: ui/dist is empty or missing — frontend build failed"
  exit 1
fi

echo "======= BUILD COMPLETE ======="
