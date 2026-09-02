#!/usr/bin/env bash
set +e

candidate_root=/candidate
trusted_root=/reference

printf 'Required untrusted provenance artifacts:\n'
for audit_name in run-input.json metrics.json codex-last.txt codex-output.log; do
  audit_path="$candidate_root/$audit_name"
  if [[ -L "$audit_path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$audit_path" "$(readlink "$audit_path")"
  elif [[ -f "$audit_path" ]]; then
    printf 'REGULAR %s\n' "$audit_path"
  elif [[ -e "$audit_path" ]]; then
    printf 'MISTYPED %s (%s)\n' "$audit_path" "$(stat -c '%F' "$audit_path")"
  else
    printf 'MISSING %s\n' "$audit_path"
  fi
done

printf '\nTrace-like candidate entries:\n'
find "$candidate_root" -maxdepth 2 \( -iname '*trace*' -o -iname '*generation*' \) \
  -printf '%y %p -> %l\n' | sort

printf '\nCandidate entry inventory:\n'
find "$candidate_root" -printf '%P\t%y\t%l\n' | sort

printf '\nTrusted entry inventory:\n'
find "$trusted_root" -printf '%P\t%y\t%l\n' | sort

printf '\nPrompt comparison:\n'
cmp --verbose "$candidate_root/prompt.py" "$trusted_root/prompt.py"
printf 'prompt_cmp_status=%d\n' "$?"

printf '\nTranslator comparison:\n'
cmp --verbose "$candidate_root/py2mpy.py" "$trusted_root/py2mpy.py"
printf 'translator_cmp_status=%d\n' "$?"

printf '\nSupplied semantics type/name comparison:\n'
diff -u \
  <(cd "$candidate_root/reference-semantics" && find . -printf '%P\t%y\t%l\n' | sort) \
  <(cd "$trusted_root/reference-semantics" && find . -printf '%P\t%y\t%l\n' | sort)
printf 'semantics_inventory_diff_status=%d\n' "$?"

printf '\nSupplied semantics recursive content comparison:\n'
diff --brief --recursive --no-dereference \
  "$candidate_root/reference-semantics" "$trusted_root/reference-semantics"
printf 'semantics_content_diff_status=%d\n' "$?"

printf '\nSupplied semantics SHA-256 values (candidate then trusted):\n'
(
  cd "$candidate_root/reference-semantics" || exit
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)
(
  cd "$trusted_root/reference-semantics" || exit
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)

printf '\nSymlink check in required candidate sources:\n'
find "$candidate_root" \
  \( -path "$candidate_root/__pycache__" -o -path "$candidate_root/__pycache__/*" \) -prune -o \
  -type l -printf 'SYMLINK %p -> %l\n'
