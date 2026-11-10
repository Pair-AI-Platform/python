#!/usr/bin/env bash
# Prints the Wolfi packages every image would get if it were built now: one "<image> <arch> <name>
# <version>" line each, sorted. The hourly watcher (wolfi-watch.yml) compares its hash with the last
# run and starts a release as soon as Wolfi has published a new version of anything in the images.
#
#   scripts/wolfi-state.sh
#
# Resolves with `apko lock`, which reads the package indexes but downloads no package. Packages built
# in this repository (melange/) are left out; Renovate tracks those.
set -euo pipefail

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

local_packages="$(sed -n 's/^  name: //p' melange/*.yaml 2>/dev/null | tr '\n' '|' | sed 's/|$//')"

for config in apko/*.apko.yaml; do
  image="$(basename "$config" .apko.yaml)"
  if [ -n "$local_packages" ]; then
    grep -vE "^\s+- (${local_packages})(=|\$)" "$config" > "$work/$image.yaml"
  else
    cp "$config" "$work/$image.yaml"
  fi
  apko lock "$work/$image.yaml" --arch x86_64,aarch64 --output "$work/$image.lock.json" >/dev/null 2>&1
  jq -r --arg image "$image" '.contents.packages[] | "\($image) \(.architecture) \(.name) \(.version)"' \
    "$work/$image.lock.json"
done | sort
