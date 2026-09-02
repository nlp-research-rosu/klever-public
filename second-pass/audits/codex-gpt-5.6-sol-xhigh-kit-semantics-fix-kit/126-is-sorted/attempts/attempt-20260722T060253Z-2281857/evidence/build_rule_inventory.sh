#!/usr/bin/env bash
set -euo pipefail

root=/tmp/audit-work/126-is-sorted

mapfile -t files < <(
  {
    printf '%s\n' "$root/reference-semantics/semantics.k"
    find "$root/reference-semantics/semantics" -maxdepth 1 -type f -name '*.k' -print | sort
    printf '%s\n' "$root/verification.k" "$root/spec.k"
  }
)

printf 'entry_kind\tsource\tline\tattributes\tdisposition\tdeclaration\n'

for path in "${files[@]}"; do
  rel=${path#"$root/"}
  case "$rel" in
    verification.k)
      disposition=REVIEWED_CANDIDATE_LOCAL
      ;;
    spec.k)
      disposition=REVIEWED_CLAIM
      ;;
    reference-semantics/semantics/concrete.k)
      disposition=SUPPLIED_CONCRETE_ONLY
      ;;
    reference-semantics/semantics.k|reference-semantics/semantics/syntax.k|reference-semantics/semantics/core.k|reference-semantics/semantics/functions.k|reference-semantics/semantics/call.k|reference-semantics/semantics/controls.k|reference-semantics/semantics/iter.k|reference-semantics/semantics/list.k|reference-semantics/semantics/bool.k|reference-semantics/semantics/int.k|reference-semantics/semantics/operators.k|reference-semantics/semantics/builtins.k|reference-semantics/semantics/tuple.k)
      disposition=SUPPLIED_USED_PATH_REVIEWED
      ;;
    *)
      disposition=SUPPLIED_UNUSED_PATH
      ;;
  esac

  awk -v source="$rel" -v disposition="$disposition" '
    function trim(s) {
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", s)
      gsub(/[[:space:]]+/, " ", s)
      return s
    }
    function flush(    attrs, cls) {
      if (!active) return
      attrs = "-"
      if (block ~ /\[([^]]*,[[:space:]]*)?function([,[:space:]\]])/) attrs = attrs ",function"
      if (block ~ /\[([^]]*,[[:space:]]*)?total([,[:space:]\]])/) attrs = attrs ",total"
      if (block ~ /\[([^]]*,[[:space:]]*)?functional([,[:space:]\]])/) attrs = attrs ",functional"
      if (block ~ /\[([^]]*,[[:space:]]*)?simplification([,[:space:]\]])/) attrs = attrs ",simplification"
      if (block ~ /priority\(/) attrs = attrs ",priority"
      if (block ~ /\[([^]]*,[[:space:]]*)?owise([,[:space:]\]])/) attrs = attrs ",owise"
      if (block ~ /\[([^]]*,[[:space:]]*)?concrete([,[:space:]\]])/) attrs = attrs ",concrete"
      if (block ~ /no-evaluators/) attrs = attrs ",opaque-no-evaluators"
      if (block ~ /\[([^]]*,[[:space:]]*)?macro([,[:space:]\]])/) attrs = attrs ",macro"
      if (block ~ /macro-rec/) attrs = attrs ",macro-rec"
      sub(/^-?,-?/, "", attrs)
      print kind "\t" source "\t" start "\t" attrs "\t" disposition "\t" first
      active = 0
      block = ""
    }
    {
      probe = $0
      sub(/^[[:space:]]+/, "", probe)
      token = probe
      sub(/[[:space:]].*$/, "", token)
      structural = (token == "configuration" || token == "syntax" || token == "context" || token == "rule" || token == "claim")
      boundary = structural || token == "module" || token == "endmodule"
      if (boundary) flush()
      if (structural) {
        active = 1
        kind = token
        start = NR
        first = trim($0)
        code = $0
        sub(/\/\/.*/, "", code)
        block = code
      } else if (active) {
        code = $0
        sub(/\/\/.*/, "", code)
        block = block "\n" code
      }
    }
    END { flush() }
  ' "$path"
done
