# Exhaustive K source inventory summary

Inventory rows: 1093

Every launcher-supplied K source statement and every proof-local `verification.k` statement is listed in `rule-inventory.csv` with source lines, attributes, reachability disposition, and review basis.

## Kinds

- concrete semantic/equational rule: 35
- configuration: 1
- endmodule: 26
- evaluation context: 5
- function syntax declaration: 121
- imports: 87
- module: 26
- opaque syntax/function declaration: 25
- ordinary semantic/equational rule: 589
- owise semantic/equational rule: 26
- priority semantic rule: 45
- requires: 24
- simplification rule: 2
- syntax declaration: 77
- syntax macro declaration: 4

## Dispositions

- CONCRETE_EVIDENCE_PATH_REVIEWED: 3
- OFF_PATH_FIXED_SEMANTICS_REVIEWED: 865
- OFF_PATH_OPAQUE_FIXED_PRIMITIVE: 24
- ON_PATH_REVIEWED_SOUND_OR_FIXED_PRIMITIVE: 194
- ON_PATH_TRUSTED_PRIMITIVE_LIMITATION: 1
- PROOF_LOCAL_REVIEWED_SOUND: 6

The two proof-local simplifications are the only local theory extensions. `sortVS` is the only on-path opaque result-bearing symbol. All other opaque symbols and off-path rules have distinct top constructors or sorts and cannot affect this claim.
