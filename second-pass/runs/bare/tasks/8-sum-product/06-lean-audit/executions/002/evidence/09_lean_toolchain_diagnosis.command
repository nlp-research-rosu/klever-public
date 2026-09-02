command -v lake || true
command -v lean || true
command -v elan || true
lake --version || true
lean --version || true
elan --version || true
elan show || true
printf 'lean-toolchain: '
sed -n '1p' /reference/klean-generation/generated/lean-toolchain
printf 'PATH entries containing elan/lean: '
printf '%s\n' "$PATH" | tr ':' '\n' | rg 'elan|lean|lake|nix' || true
