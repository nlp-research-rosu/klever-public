#!/usr/bin/env python3
"""Source facts supporting the auditor's two independent classifications."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


ROOT = Path("/reference/k-proof")
inventory = inventory_verification(ROOT)
verification = (ROOT / "verification.k").read_text()
solution_mpy = (ROOT / "solution.mpy").read_text()
solution_py = (ROOT / "solution.py").read_text()
spec = (ROOT / "spec.k").read_text()
core = (ROOT / "reference-semantics/semantics/core.k").read_text()
functions = (ROOT / "reference-semantics/semantics/functions.k").read_text()
call = (ROOT / "reference-semantics/semantics/call.k").read_text()
builtins = (ROOT / "reference-semantics/semantics/builtins.k").read_text()

definition, operational = inventory["rules"]
definition_rhs = definition["text"].split("=>", 1)[1]

checks = {
    "exactly_two_local_closure_rules": len(inventory["rules"]) == 2,
    "definition_symbol_declared_macro": (
        'syntax Module ::= "strlenModule" [macro]' in verification
    ),
    "definition_rhs_is_exact_solution_module": (
        re.sub(r"\s+", "", definition_rhs)
        == re.sub(r"\s+", "", solution_mpy)
    ),
    "source_solution_calls_builtin_len": (
        "return len(string)" in solution_py
    ),
    "operational_rule_is_k_cell_transition": (
        "<k> #invokeStrlen(V:Val)" in operational["text"]
    ),
    "operational_rule_loads_exact_macro": (
        "#loadAll(strlenModule)" in operational["text"]
    ),
    "operational_rule_calls_public_function_with_same_value": (
        'Call(Name("strlen"), V)' in operational["text"]
    ),
    "operational_rule_does_not_assume_postcondition": (
        "isLen" not in operational["text"]
    ),
    "spec_starts_from_operational_harness": (
        "<k> #invokeStrlen(str(S:IntSeq)) => isLen(S) </k>" in spec
    ),
    "semantics_loads_module_statements": (
        "#loadAll(Module(SS:Stmts)) => SS" in core
    ),
    "semantics_installs_function_closure": (
        "F <- closureVal(PNS, BODY, L)" in functions
    ),
    "semantics_uses_normal_call_route": (
        "Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS)" in call
    ),
    "semantics_dispatches_closure_body": (
        "#bindP(PNS, ACC) ~> BODY ~> #endcall" in call
    ),
    "semantics_resolves_len_as_builtin": (
        '"len"    <- builtinV("len")' in core
    ),
    "semantics_len_of_string_is_isLen": (
        'seqLen(str(IS:IntSeq))                   => isLen(IS)' in builtins
    ),
    "semantics_isLen_has_base_and_recurrence": (
        "isLen(.IntSeq)                => 0" in core
        and "isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)" in core
    ),
    "neither_rule_is_simplification": all(
        "simplification" not in rule["attributes"]
        for rule in inventory["rules"]
    ),
    "no_rule_is_a_claim_or_derived_lemma": all(
        rule["text"].lstrip().startswith("rule ")
        for rule in inventory["rules"]
    ),
}

print(
    json.dumps(
        {
            "all_checks_pass": all(checks.values()),
            "checks": checks,
            "judgments": [
                {
                    "source_rule_id": definition["source_rule_id"],
                    "classification": "DEFINITION",
                    "reason": (
                        "It is the expansion equation for the named "
                        "[macro] term strlenModule and its RHS is the exact "
                        "translated source module."
                    ),
                },
                {
                    "source_rule_id": operational["source_rule_id"],
                    "classification": "OPERATIONAL_RULE",
                    "reason": (
                        "It is a k-cell harness step that loads the exact "
                        "module and invokes the source function through the "
                        "ordinary supplied call semantics; it states no "
                        "mathematical shortcut or postcondition."
                    ),
                },
            ],
            "true_domain_lemmas": [],
            "proved_derived_lemmas": [],
        },
        indent=2,
        sort_keys=True,
    )
)
