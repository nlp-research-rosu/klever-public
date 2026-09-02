#!/usr/bin/env python3
"""Mechanical part of the independent Stage 5 operational-binding audit."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools import k_rule_inventory

PROOF = Path("/candidate/Proof.lean")
OPERATIONAL = Path("/candidate/Proof/Operational.lean")
MANIFEST = Path("/reference/klean-generation/generator-manifest.json")
STAGE1 = Path("/reference/k-proof")

EXPECTED = {
    "_andBool_": ("boolAndImpl", "Boolean conjunction"),
    "_orBool_": ("boolOrImpl", "Boolean disjunction"),
    "«_>Int_»": ("intGreaterImpl", "strict mathematical-integer order"),
    "«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»": ("cmpDispatchImpl", "MPY comparison dispatch on represented Val constructors"),
    "«codesOf(_)_VERIFICATION_IntSeq_Str»": ("codesFromStrImpl", "unwrap the str(IntSeq) constructor"),
    "isBool": ("isBoolImpl", "exact singleton-K-sequence Bool sort test"),
    "isFloat": ("isFloatImpl", "exact singleton-K-sequence Float sort test"),
    "isInt": ("isIntImpl", "exact singleton-K-sequence Int sort test"),
    "«isNumericV(_)_VERIFICATION_Bool_Val»": ("numericImpl", "Int/Bool/Float Val union, excluding all others"),
    "isStr": ("isStrImpl", "exact singleton-K-sequence Str sort test"),
    "maxFOpaque": ("floatMaxImpl", "K FLOAT.max concrete behavior"),
    "«maxFloat(_,_)_FLOAT_Float_Float_Float»": ("floatMaxImpl", "K FLOAT.max concrete behavior"),
    "«numericGt(_,_)_VERIFICATION_Bool_NumericView_NumericView»": ("numericGreaterImpl", "frozen exhaustive NumericView strict-order table"),
    "«numericView(_)_VERIFICATION_NumericView_Val»": ("numericViewImpl", "frozen disjoint Int/Bool/Float/other tagged view"),
    "«project:Bool»": ("boolProjectionImpl", "guarded Bool projection"),
    "«project:Float»": ("floatProjectionImpl", "guarded Float projection"),
    "«project:Int»": ("intProjectionImpl", "guarded Int projection"),
    "«project:Str»": ("strProjectionImpl", "guarded Str projection"),
    "projectBoolTotal": ("boolTotalProjectionImpl", "Bool payload on its frozen guard"),
    "projectFloatTotal": ("floatTotalProjectionImpl", "Float payload on its frozen guard"),
    "projectIntTotal": ("intTotalProjectionImpl", "Int payload on its frozen guard"),
    "projectStrTotal": ("strTotalProjectionImpl", "Str payload on its frozen guard"),
    "«strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq»": ("strLessImpl", "strict lexicographic code-point order"),
    "«project:Bool?»": ("boolProjectionOptImpl", "partial Bool projection as Option"),
    "«project:Float?»": ("floatProjectionOptImpl", "partial Float projection as Option"),
    "«project:Int?»": ("intProjectionOptImpl", "partial Int projection as Option"),
    "«project:Str?»": ("strProjectionOptImpl", "partial Str projection as Option"),
}


def fail(message: str) -> None:
    raise SystemExit("FAIL " + message)


def main() -> None:
    proof_text = PROOF.read_text()
    operational_text = OPERATIONAL.read_text()
    target = json.loads(MANIFEST.read_text())["target"]
    inventory = k_rule_inventory.inventory_verification(STAGE1)
    rules = {entry["source_rule_id"]: entry for entry in inventory["rules"]}

    found: dict[str, str] = {}
    pattern = re.compile(
        r"^(?:noncomputable )?def (.+?) : .*? := Operational\.([A-Za-z0-9_]+)$",
        re.MULTILINE,
    )
    for name, implementation in pattern.findall(proof_text):
        if name in found:
            fail(f"duplicate candidate binding {name}")
        found[name] = implementation

    manifest_names = [item["name"] for item in target["parameters"]]
    if manifest_names != list(EXPECTED):
        fail("manifest parameter order/name sequence differs from independent matrix")
    if set(found) != set(manifest_names):
        fail(f"candidate binding set mismatch: missing={set(manifest_names)-set(found)}, extra={set(found)-set(manifest_names)}")
    if proof_text.count("targetStatement") != 2:
        fail("candidate targetStatement reference count is not theorem type plus unfold")
    if re.search(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", proof_text + "\n" + operational_text):
        fail("forbidden trust escape in candidate source")

    print("COMMAND: PYTHONPATH=/reference python3 /audit-output/evidence/bridge_audit.py")
    print(f"inventory_sha256={inventory['inventory_sha256']}")
    print(f"target_statement_sha256={target['statement_sha256']}")
    print(f"parameter_count={len(manifest_names)}")
    for index, parameter in enumerate(target["parameters"], 1):
        name = parameter["name"]
        expected_impl, judgment = EXPECTED[name]
        observed_impl = found[name]
        if observed_impl != expected_impl:
            fail(f"{name}: observed Operational.{observed_impl}, expected Operational.{expected_impl}")
        if not re.search(rf"^(?:noncomputable )?def {re.escape(expected_impl)}\b", operational_text, re.MULTILINE):
            fail(f"missing exact candidate definition Operational.{expected_impl}")
        print(f"BINDING {index:02d}: PASS {name} -> Operational.{observed_impl}")
        print(f"  kore_symbol={parameter['kore_symbol']}")
        print(f"  semantic_judgment={judgment}")
        for source_id in parameter["source_rule_ids"]:
            if source_id not in rules:
                fail(f"{name}: source rule absent from independently reconstructed inventory: {source_id}")
            rule = rules[source_id]
            print(f"  source={source_id} verification.k:{rule['start_line']}-{rule['end_line']}")
            print("    " + " ".join(rule["text"].split()))
    print("PASS operational binding names, implementations, KORE symbols, and source-rule links: 27/27")


if __name__ == "__main__":
    main()
