#!/usr/bin/env bash
set -u
echo '$ sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py'
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
echo '$ sed -n "1,320p" /reference/generation-tools/source-manifest.json'
sed -n '1,320p' /reference/generation-tools/source-manifest.json
echo '$ sed -n "1,360p" /reference/klean-generation/generator-manifest.json'
sed -n '1,360p' /reference/klean-generation/generator-manifest.json
echo '$ sed -n "1,320p" /reference/klean-generation/input-manifest.json'
sed -n '1,320p' /reference/klean-generation/input-manifest.json
echo '$ sed -n "1,280p" /reference/klean-generation/export-result.json'
sed -n '1,280p' /reference/klean-generation/export-result.json
echo '$ sha256sum /reference/generation-tools/source-manifest.json /reference/klean-generation/generator-manifest.json /reference/klean-generation/input-manifest.json /reference/klean-generation/export-result.json'
sha256sum /reference/generation-tools/source-manifest.json /reference/klean-generation/generator-manifest.json /reference/klean-generation/input-manifest.json /reference/klean-generation/export-result.json
