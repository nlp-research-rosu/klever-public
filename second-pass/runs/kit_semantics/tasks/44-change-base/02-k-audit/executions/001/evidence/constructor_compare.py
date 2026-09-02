#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


def canonical_digest(term) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def walk(term):
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def label_name(term):
    if not isinstance(term, dict) or term.get("node") != "KApply":
        return None
    return term.get("label", {}).get("name")


solution_data = json.loads(
    Path("/tmp/audit-work/44-change-base/solution-parsed.json").read_text()
)
spec_data = json.loads(
    Path("/tmp/audit-work/44-change-base/spec-parsed.json").read_text()
)

func_defs = [
    term
    for term in walk(solution_data["term"])
    if label_name(term) == "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"
]
if len(func_defs) != 1:
    raise RuntimeError(f"expected one FuncDef, found {len(func_defs)}")
func_def = func_defs[0]
name_term, params_wrapper, program_body = func_def["args"]
program_params = params_wrapper["args"][0]
program_name = name_term["token"]

claims = spec_data["term"]["term"][0]["localSentences"]
print(f"solution_function_count={len(func_defs)}")
print(f"solution_function_name={program_name}")
print(f"solution_params_sha256={canonical_digest(program_params)}")
print(f"solution_body_sha256={canonical_digest(program_body)}")
print(f"claim_count={len(claims)}")

failures = []
for claim in claims:
    attrs = claim["att"]["att"]
    claim_label = attrs.get("label", "<missing-label>")
    closures = [
        term
        for term in walk(claim["body"])
        if label_name(term)
        == "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
    ]
    print(f"claim={claim_label} closure_count={len(closures)}")
    if len(closures) != 1:
        failures.append(f"{claim_label}: expected one closure, found {len(closures)}")
        continue
    claim_params, claim_body, defining_env = closures[0]["args"]
    params_equal = claim_params == program_params
    body_equal = claim_body == program_body
    defining_env_is_zero = (
        defining_env.get("node") == "KToken"
        and defining_env.get("sort", {}).get("name") == "Int"
        and defining_env.get("token") == "0"
    )
    print(
        f"claim={claim_label} params_sha256={canonical_digest(claim_params)} "
        f"body_sha256={canonical_digest(claim_body)}"
    )
    print(
        f"claim={claim_label} params_equal={params_equal} "
        f"body_equal={body_equal} defining_env_is_zero={defining_env_is_zero}"
    )
    if not (params_equal and body_equal and defining_env_is_zero):
        failures.append(f"{claim_label}: closure does not pin submitted body")

entry_claims = [
    claim
    for claim in claims
    if claim["att"]["att"].get("label") == "SPEC.change-base"
]
if len(entry_claims) != 1:
    failures.append(f"expected one entry claim, found {len(entry_claims)}")
else:
    entry = entry_claims[0]
    all_call_terms = [
        term
        for term in walk(entry["body"])
        if label_name(term) == "Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs"
    ]
    call_terms = []
    for term in all_call_terms:
        callee = term["args"][0]
        if (
            label_name(callee) == "Name(_)_MPY-SYNTAX_Expr_String"
            and callee["args"][0].get("token") == '"change_base"'
        ):
            call_terms.append(term)
    summary_terms = [
        term
        for term in walk(entry["body"])
        if label_name(term)
        == "changeBaseCodes(_,_)_VERIFICATION_IntSeq_Int_Int"
    ]
    print(f"entry_all_call_term_count={len(all_call_terms)}")
    print(f"entry_change_base_call_term_count={len(call_terms)}")
    print(f"entry_changeBaseCodes_count={len(summary_terms)}")
    if len(call_terms) != 1 or len(summary_terms) != 1:
        failures.append("entry claim lacks unique call or result summary")

print(f"FAILURE_COUNT={len(failures)}")
for failure in failures:
    print(f"FAILURE: {failure}")
raise SystemExit(1 if failures else 0)
