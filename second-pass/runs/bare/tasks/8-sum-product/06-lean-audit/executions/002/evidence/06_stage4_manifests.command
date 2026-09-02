for audit_file in \
  /reference/klean-generation/input-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/preflight.json \
  /reference/klean-generation/trust-inventory.json \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-toolchain.lock.json
do
  printf '\nFILE %s\n' "$audit_file"
  sha256sum "$audit_file"
  python3 -m json.tool "$audit_file"
done
printf '\nGENERATED LEAN SOURCES\n'
for audit_file in $(rg --files /reference/klean-generation/generated | rg '\.lean$' | sort)
do
  printf '\nFILE %s\n' "$audit_file"
  sha256sum "$audit_file"
  nl -ba "$audit_file"
done
