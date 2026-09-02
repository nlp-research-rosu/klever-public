# Exhaustive local K sentence inventory

Files: 26
Records: 1160

## Counts

- `claim`: 5
- `configuration`: 1
- `context`: 5
- `endmodule`: 27
- `imports`: 88
- `module`: 27
- `requires`: 25
- `rule`: 740
- `syntax`: 242

## Review decisions

- `EXACT_MACRO`: 14
- `FIXED_SUPPLIED_CONCRETE_ONLY`: 24
- `FIXED_SUPPLIED_MATERIAL_MODULE`: 352
- `FIXED_SUPPLIED_UNUSED_MODULE`: 711
- `INPUT_REPRESENTATION_SYMBOL`: 1
- `LIMITED_TOTALITY_DECLARATION`: 2
- `OPERATIONAL_BRIDGE_EVIDENCE_GAP`: 1
- `POSITIVE_REACHABILITY_CLAIM`: 5
- `SOUND_DEFINITIONAL_SUMMARY`: 19
- `SOUND_DOMAIN_SYNTAX`: 1
- `SOUND_FIXED_RULE_SPECIALIZATION`: 20
- `SOUND_INPUT_REPRESENTATION_RULE`: 2
- `SPEC_STRUCTURE`: 4
- `STRUCTURE`: 4

## Records

### reference-semantics/semantics.k:34:bd63dc2187be

- Kind: `requires`
- Lines: 34-34
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/syntax.k"
```

### reference-semantics/semantics.k:35:8224539e3a3d

- Kind: `requires`
- Lines: 35-35
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/core.k"
```

### reference-semantics/semantics.k:36:1e5b8702816a

- Kind: `requires`
- Lines: 36-36
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/iter.k"
```

### reference-semantics/semantics.k:37:aa5f663a5d1a

- Kind: `requires`
- Lines: 37-37
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/range.k"
```

### reference-semantics/semantics.k:38:b194c4171e7a

- Kind: `requires`
- Lines: 38-38
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/operators.k"
```

### reference-semantics/semantics.k:39:821ae9d706d1

- Kind: `requires`
- Lines: 39-39
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/int.k"
```

### reference-semantics/semantics.k:40:4486f908787b

- Kind: `requires`
- Lines: 40-40
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/bool.k"
```

### reference-semantics/semantics.k:41:c686ca866c6c

- Kind: `requires`
- Lines: 41-41
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/float.k"
```

### reference-semantics/semantics.k:42:3e6d049d0d07

- Kind: `requires`
- Lines: 42-42
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/str.k"
```

### reference-semantics/semantics.k:43:28167624a987

- Kind: `requires`
- Lines: 43-43
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/set.k"
```

### reference-semantics/semantics.k:44:a95bd351b20c

- Kind: `requires`
- Lines: 44-44
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/list.k"
```

### reference-semantics/semantics.k:45:4a702fffa1e1

- Kind: `requires`
- Lines: 45-45
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/tuple.k"
```

### reference-semantics/semantics.k:46:f795613d9cb1

- Kind: `requires`
- Lines: 46-46
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/subscript.k"
```

### reference-semantics/semantics.k:47:927b4eb4e3dc

- Kind: `requires`
- Lines: 47-47
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/comprehension.k"
```

### reference-semantics/semantics.k:48:3708c0fc4fe9

- Kind: `requires`
- Lines: 48-48
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/methods.k"
```

### reference-semantics/semantics.k:49:498f2b091406

- Kind: `requires`
- Lines: 49-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/controls.k"
```

### reference-semantics/semantics.k:50:bf13fda77786

- Kind: `requires`
- Lines: 50-50
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/functions.k"
```

### reference-semantics/semantics.k:51:9dc1130a72c5

- Kind: `requires`
- Lines: 51-51
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/builtins.k"
```

### reference-semantics/semantics.k:52:666c60af66b9

- Kind: `requires`
- Lines: 52-52
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/call.k"
```

### reference-semantics/semantics.k:53:9879ce98eb66

- Kind: `requires`
- Lines: 53-53
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/sort.k"
```

### reference-semantics/semantics.k:54:d0eef04114b1

- Kind: `requires`
- Lines: 54-54
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/assert.k"
```

### reference-semantics/semantics.k:55:dff85649217f

- Kind: `requires`
- Lines: 55-55
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/dict.k"
```

### reference-semantics/semantics.k:56:f5f94e239ba7

- Kind: `requires`
- Lines: 56-56
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
requires "semantics/concrete.k"
```

### reference-semantics/semantics.k:58:340f552bdab1

- Kind: `module`
- Lines: 58-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY
```

### reference-semantics/semantics.k:59:4258a966960e

- Kind: `imports`
- Lines: 59-59
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CORE
```

### reference-semantics/semantics.k:60:8ad41781e06e

- Kind: `imports`
- Lines: 60-60
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-ITER
```

### reference-semantics/semantics.k:61:548212ddc441

- Kind: `imports`
- Lines: 61-61
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-RANGE
```

### reference-semantics/semantics.k:62:ee018db6efb0

- Kind: `imports`
- Lines: 62-62
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-OPERATORS
```

### reference-semantics/semantics.k:63:6a7df951c212

- Kind: `imports`
- Lines: 63-63
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-INT
```

### reference-semantics/semantics.k:64:bdd3eb0c1e7c

- Kind: `imports`
- Lines: 64-64
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-BOOL
```

### reference-semantics/semantics.k:65:b6b71fc553a1

- Kind: `imports`
- Lines: 65-65
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-FLOAT
```

### reference-semantics/semantics.k:66:1c022ad4e0c9

- Kind: `imports`
- Lines: 66-66
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-STR
```

### reference-semantics/semantics.k:67:783147658ae8

- Kind: `imports`
- Lines: 67-67
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-SET
```

### reference-semantics/semantics.k:68:511c798e04e9

- Kind: `imports`
- Lines: 68-68
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-LIST
```

### reference-semantics/semantics.k:69:b1d1ddeb005d

- Kind: `imports`
- Lines: 69-69
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-TUPLE
```

### reference-semantics/semantics.k:70:e90331404c5d

- Kind: `imports`
- Lines: 70-70
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-SUBSCRIPT
```

### reference-semantics/semantics.k:71:18c619c21645

- Kind: `imports`
- Lines: 71-71
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-COMPREHENSION
```

### reference-semantics/semantics.k:72:09fe9e0706ae

- Kind: `imports`
- Lines: 72-72
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-METHODS
```

### reference-semantics/semantics.k:73:47dfd92e317b

- Kind: `imports`
- Lines: 73-73
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CONTROLS
```

### reference-semantics/semantics.k:74:62b2a9826516

- Kind: `imports`
- Lines: 74-74
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-FUNCTIONS
```

### reference-semantics/semantics.k:75:513b07985ad1

- Kind: `imports`
- Lines: 75-75
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-BUILTINS
```

### reference-semantics/semantics.k:76:0c52765c8867

- Kind: `imports`
- Lines: 76-76
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CALL
```

### reference-semantics/semantics.k:77:051aad84a25d

- Kind: `imports`
- Lines: 77-77
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-SORT
```

### reference-semantics/semantics.k:78:4f603401acfe

- Kind: `imports`
- Lines: 78-78
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-ASSERT
```

### reference-semantics/semantics.k:79:4ff989d72f49

- Kind: `imports`
- Lines: 79-79
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-DICT
```

### reference-semantics/semantics.k:80:85f16bdbb9c7

- Kind: `endmodule`
- Lines: 80-86
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule

// The krun (llvm) main module: MPY plus the concrete-only legs (keyed sort's
// real key calls, deep list equality). Verification builds import MPY and
// never see MPY-CONCRETE. The llvm kompile MUST use --main-module MPY-KRUN —
// with plain MPY the concrete legs are silently absent (this was live for a
// while: sorted-key stuck and comprehension asserted wrong under krun).
```

### reference-semantics/semantics.k:87:3c507e22c3e1

- Kind: `module`
- Lines: 87-87
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-KRUN
```

### reference-semantics/semantics.k:88:6ae4e1db797b

- Kind: `imports`
- Lines: 88-88
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY
```

### reference-semantics/semantics.k:89:ed62b27710df

- Kind: `imports`
- Lines: 89-89
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CONCRETE
```

### reference-semantics/semantics.k:90:4c5df27adc71

- Kind: `endmodule`
- Lines: 90-90
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/assert.k:3:c9be78fdc587

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-ASSERT
```

### reference-semantics/semantics/assert.k:4:4258a966960e

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/assert.k:6:90fd8cb48806

- Kind: `rule`
- Lines: 6-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### reference-semantics/semantics/assert.k:8:dfe24d6909ca

- Kind: `rule`
- Lines: 8-11
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### reference-semantics/semantics/assert.k:13:94ec1f9b3215

- Kind: `rule`
- Lines: 13-15
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/assert.k:16:4c5df27adc71

- Kind: `endmodule`
- Lines: 16-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/bool.k:5:d0f4ccd7f134

- Kind: `module`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-BOOL
```

### reference-semantics/semantics/bool.k:6:4258a966960e

- Kind: `imports`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/bool.k:8:f6a9f817afd5

- Kind: `rule`
- Lines: 8-8
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### reference-semantics/semantics/bool.k:10:27c7ab073847

- Kind: `rule`
- Lines: 10-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### reference-semantics/semantics/bool.k:11:331c5ccbdb8e

- Kind: `rule`
- Lines: 11-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### reference-semantics/semantics/bool.k:16:4bad2e2ff81c

- Kind: `context`
- Lines: 16-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### reference-semantics/semantics/bool.k:17:dd652a87b566

- Kind: `rule`
- Lines: 17-17
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### reference-semantics/semantics/bool.k:18:c903d941fb73

- Kind: `rule`
- Lines: 18-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### reference-semantics/semantics/bool.k:20:609b42dde8ce

- Kind: `rule`
- Lines: 20-21
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### reference-semantics/semantics/bool.k:22:66ef890f68fe

- Kind: `rule`
- Lines: 22-23
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### reference-semantics/semantics/bool.k:24:a1e1d5c0c320

- Kind: `rule`
- Lines: 24-28
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

### reference-semantics/semantics/bool.k:29:570c438ed2f8

- Kind: `rule`
- Lines: 29-30
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/bool.k:31:b20811d55420

- Kind: `rule`
- Lines: 31-34
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### reference-semantics/semantics/bool.k:35:1da617ae2897

- Kind: `rule`
- Lines: 35-38
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### reference-semantics/semantics/bool.k:39:2eb620e8bf34

- Kind: `rule`
- Lines: 39-42
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### reference-semantics/semantics/bool.k:43:86c2967b9fc6

- Kind: `rule`
- Lines: 43-46
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### reference-semantics/semantics/bool.k:47:4c5df27adc71

- Kind: `endmodule`
- Lines: 47-47
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/builtins.k:3:714fcf7fc40f

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-BUILTINS
```

### reference-semantics/semantics/builtins.k:4:4258a966960e

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/builtins.k:5:1c022ad4e0c9

- Kind: `imports`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-STR
```

### reference-semantics/semantics/builtins.k:6:783147658ae8

- Kind: `imports`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-SET
```

### reference-semantics/semantics/builtins.k:7:8ad41781e06e

- Kind: `imports`
- Lines: 7-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-ITER
```

### reference-semantics/semantics/builtins.k:8:548212ddc441

- Kind: `imports`
- Lines: 8-8
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-RANGE
```

### reference-semantics/semantics/builtins.k:9:6a7df951c212

- Kind: `imports`
- Lines: 9-9
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-INT
```

### reference-semantics/semantics/builtins.k:10:481e0c655538

- Kind: `imports`
- Lines: 10-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-METHODS

  // the builtins REGISTRY is core.k's builtinsScope (the -1 frame); names resolve by lookup

  // Call routing + argument evaluation live in call.k, which also routes the fold
  // builtins (sum/all/any/max/min) to the #_Acc folds below and everything else to
  // applyBuiltin. This module owns applyBuiltin + the fold implementations.
```

### reference-semantics/semantics/builtins.k:17:73578867deee

- Kind: `syntax`
- Lines: 17-19
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### reference-semantics/semantics/builtins.k:20:f6cf3d1713c1

- Kind: `syntax`
- Lines: 20-20
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= seqLen(Val) [function]
```

### reference-semantics/semantics/builtins.k:21:4c33466e09a7

- Kind: `rule`
- Lines: 21-21
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### reference-semantics/semantics/builtins.k:22:0aaba3d3b63a

- Kind: `rule`
- Lines: 22-22
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### reference-semantics/semantics/builtins.k:23:f5cd3a9a635b

- Kind: `rule`
- Lines: 23-23
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### reference-semantics/semantics/builtins.k:24:d643ec5ddd39

- Kind: `rule`
- Lines: 24-24
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### reference-semantics/semantics/builtins.k:25:fe3adc7a7e15

- Kind: `rule`
- Lines: 25-25
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### reference-semantics/semantics/builtins.k:26:66ce929da75b

- Kind: `rule`
- Lines: 26-31
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### reference-semantics/semantics/builtins.k:32:200f6d489286

- Kind: `rule`
- Lines: 32-32
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### reference-semantics/semantics/builtins.k:33:d4c8072f0224

- Kind: `rule`
- Lines: 33-33
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### reference-semantics/semantics/builtins.k:34:0b80f78f2b97

- Kind: `rule`
- Lines: 34-34
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### reference-semantics/semantics/builtins.k:35:8b7fa386647f

- Kind: `rule`
- Lines: 35-35
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### reference-semantics/semantics/builtins.k:36:01aff6eecdd4

- Kind: `syntax`
- Lines: 36-36
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:37:b46c475391e5

- Kind: `rule`
- Lines: 37-37
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### reference-semantics/semantics/builtins.k:38:5e4a1af2608e

- Kind: `rule`
- Lines: 38-40
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### reference-semantics/semantics/builtins.k:41:4a4f32b78920

- Kind: `rule`
- Lines: 41-43
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### reference-semantics/semantics/builtins.k:44:db3d75b51d53

- Kind: `rule`
- Lines: 44-46
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### reference-semantics/semantics/builtins.k:47:8faa5250ed2b

- Kind: `syntax`
- Lines: 47-47
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### reference-semantics/semantics/builtins.k:48:cd531bdb9afa

- Kind: `rule`
- Lines: 48-48
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### reference-semantics/semantics/builtins.k:49:74ff8e8be842

- Kind: `rule`
- Lines: 49-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### reference-semantics/semantics/builtins.k:50:1ea66d1c87c6

- Kind: `rule`
- Lines: 50-52
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### reference-semantics/semantics/builtins.k:54:0355f95a50a6

- Kind: `syntax`
- Lines: 54-54
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= intOf(Val) [function]
```

### reference-semantics/semantics/builtins.k:55:619051750e3b

- Kind: `rule`
- Lines: 55-55
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intOf(I:Int)  => I
```

### reference-semantics/semantics/builtins.k:56:4ab92a36ddc9

- Kind: `rule`
- Lines: 56-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### reference-semantics/semantics/builtins.k:59:ed695fa0c4db

- Kind: `syntax`
- Lines: 59-59
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### reference-semantics/semantics/builtins.k:60:e7fc3b9b3a84

- Kind: `rule`
- Lines: 60-60
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### reference-semantics/semantics/builtins.k:61:b74e515d3e67

- Kind: `rule`
- Lines: 61-61
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### reference-semantics/semantics/builtins.k:62:beb3eb90ee0f

- Kind: `rule`
- Lines: 62-63
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### reference-semantics/semantics/builtins.k:64:942b3c5ca939

- Kind: `rule`
- Lines: 64-65
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### reference-semantics/semantics/builtins.k:67:fbd45cd7894a

- Kind: `syntax`
- Lines: 67-67
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### reference-semantics/semantics/builtins.k:68:ca3f3bc3212a

- Kind: `rule`
- Lines: 68-68
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### reference-semantics/semantics/builtins.k:69:c0ee3d29de0f

- Kind: `rule`
- Lines: 69-69
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### reference-semantics/semantics/builtins.k:70:6d518d4a9ce7

- Kind: `rule`
- Lines: 70-71
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### reference-semantics/semantics/builtins.k:72:164008b49bd9

- Kind: `rule`
- Lines: 72-75
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

### reference-semantics/semantics/builtins.k:76:e3461106d962

- Kind: `syntax`
- Lines: 76-76
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### reference-semantics/semantics/builtins.k:77:59848da8989b

- Kind: `rule`
- Lines: 77-77
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### reference-semantics/semantics/builtins.k:78:ea3939e11fae

- Kind: `rule`
- Lines: 78-79
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### reference-semantics/semantics/builtins.k:80:66b9fabf71fa

- Kind: `rule`
- Lines: 80-80
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### reference-semantics/semantics/builtins.k:81:45675f8137ef

- Kind: `rule`
- Lines: 81-81
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### reference-semantics/semantics/builtins.k:82:fee6fab3ed0c

- Kind: `rule`
- Lines: 82-84
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### reference-semantics/semantics/builtins.k:86:612c7bdfd2d3

- Kind: `syntax`
- Lines: 86-86
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### reference-semantics/semantics/builtins.k:87:eb6389d2a176

- Kind: `rule`
- Lines: 87-87
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### reference-semantics/semantics/builtins.k:88:626486127c45

- Kind: `rule`
- Lines: 88-89
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### reference-semantics/semantics/builtins.k:90:20c0d7b936a1

- Kind: `rule`
- Lines: 90-90
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### reference-semantics/semantics/builtins.k:91:3f472924a83d

- Kind: `rule`
- Lines: 91-91
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### reference-semantics/semantics/builtins.k:92:a9b5772d35f7

- Kind: `rule`
- Lines: 92-96
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

### reference-semantics/semantics/builtins.k:97:4282c4747876

- Kind: `syntax`
- Lines: 97-97
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### reference-semantics/semantics/builtins.k:98:16f482b70cca

- Kind: `rule`
- Lines: 98-98
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### reference-semantics/semantics/builtins.k:99:d3dcf3e3dfc1

- Kind: `rule`
- Lines: 99-99
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule maxVals(M:Int, .Vals)           => M
```

### reference-semantics/semantics/builtins.k:100:f1bf63869c2f

- Kind: `rule`
- Lines: 100-100
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### reference-semantics/semantics/builtins.k:102:8b1e9d6e3b83

- Kind: `syntax`
- Lines: 102-102
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### reference-semantics/semantics/builtins.k:103:92b52ecacf4f

- Kind: `rule`
- Lines: 103-103
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### reference-semantics/semantics/builtins.k:104:a772c1fa6c19

- Kind: `rule`
- Lines: 104-104
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule minVals(M:Int, .Vals)           => M
```

### reference-semantics/semantics/builtins.k:105:52f70ac7a1b5

- Kind: `rule`
- Lines: 105-107
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### reference-semantics/semantics/builtins.k:108:75cdd7f2c5dd

- Kind: `rule`
- Lines: 108-110
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

### reference-semantics/semantics/builtins.k:111:edb0bd1ec983

- Kind: `rule`
- Lines: 111-113
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### reference-semantics/semantics/builtins.k:114:c616aba4766f

- Kind: `syntax`
- Lines: 114-114
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### reference-semantics/semantics/builtins.k:115:4e15dfee6cc6

- Kind: `rule`
- Lines: 115-115
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### reference-semantics/semantics/builtins.k:116:7e1227c3ef64

- Kind: `rule`
- Lines: 116-116
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### reference-semantics/semantics/builtins.k:117:939453dbc7b8

- Kind: `syntax`
- Lines: 117-117
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:118:7503c649eb67

- Kind: `rule`
- Lines: 118-118
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### reference-semantics/semantics/builtins.k:119:d28a9bf00ef6

- Kind: `rule`
- Lines: 119-123
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

### reference-semantics/semantics/builtins.k:124:e69569e78ca6

- Kind: `rule`
- Lines: 124-125
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### reference-semantics/semantics/builtins.k:126:aeb5f1496dff

- Kind: `syntax`
- Lines: 126-126
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:127:4833a908272d

- Kind: `rule`
- Lines: 127-127
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### reference-semantics/semantics/builtins.k:128:b2ea4cb432ba

- Kind: `rule`
- Lines: 128-131
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### reference-semantics/semantics/builtins.k:132:67a2cd9a5933

- Kind: `rule`
- Lines: 132-133
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### reference-semantics/semantics/builtins.k:134:0513f86f41d9

- Kind: `syntax`
- Lines: 134-134
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:135:289c1f881385

- Kind: `rule`
- Lines: 135-135
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### reference-semantics/semantics/builtins.k:136:74f471f298ee

- Kind: `rule`
- Lines: 136-136
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### reference-semantics/semantics/builtins.k:137:7030258d8cf7

- Kind: `rule`
- Lines: 137-139
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### reference-semantics/semantics/builtins.k:140:3651afde140b

- Kind: `rule`
- Lines: 140-142
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### reference-semantics/semantics/builtins.k:143:c4bb6edca951

- Kind: `rule`
- Lines: 143-143
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### reference-semantics/semantics/builtins.k:144:b6c400524bf5

- Kind: `rule`
- Lines: 144-147
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

### reference-semantics/semantics/builtins.k:148:514da827df95

- Kind: `rule`
- Lines: 148-148
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### reference-semantics/semantics/builtins.k:149:b3fb91d4c51d

- Kind: `rule`
- Lines: 149-151
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### reference-semantics/semantics/builtins.k:152:2c3c6d6b9c04

- Kind: `rule`
- Lines: 152-155
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

### reference-semantics/semantics/builtins.k:156:4c392478d60e

- Kind: `rule`
- Lines: 156-157
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### reference-semantics/semantics/builtins.k:158:5400597dd0d2

- Kind: `syntax`
- Lines: 158-158
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:159:cef2f51a1185

- Kind: `rule`
- Lines: 159-159
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### reference-semantics/semantics/builtins.k:160:d9500696d634

- Kind: `rule`
- Lines: 160-162
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### reference-semantics/semantics/builtins.k:163:d3b8ae0c04fe

- Kind: `rule`
- Lines: 163-163
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### reference-semantics/semantics/builtins.k:164:042e91cd858c

- Kind: `rule`
- Lines: 164-166
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### reference-semantics/semantics/builtins.k:167:8cb29bfb4210

- Kind: `rule`
- Lines: 167-168
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### reference-semantics/semantics/builtins.k:169:d3f91e2ffaf3

- Kind: `rule`
- Lines: 169-169
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:170:84cabfd28956

- Kind: `rule`
- Lines: 170-170
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:171:b15b1c71a43b

- Kind: `rule`
- Lines: 171-172
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### reference-semantics/semantics/builtins.k:173:33a124c306f4

- Kind: `rule`
- Lines: 173-173
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:174:ad218665aa87

- Kind: `rule`
- Lines: 174-176
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### reference-semantics/semantics/builtins.k:177:d63eee230cc9

- Kind: `rule`
- Lines: 177-177
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### reference-semantics/semantics/builtins.k:178:b65792b63b52

- Kind: `rule`
- Lines: 178-178
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### reference-semantics/semantics/builtins.k:179:a1fdf4df0f8e

- Kind: `rule`
- Lines: 179-186
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0

  // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
  // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
  // trusted pass evaluator, now DEFINED in the reference and driven by a
  // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
  // argument leaves the call unevaluated for problem-level folds.
```

### reference-semantics/semantics/builtins.k:187:3115789003f5

- Kind: `rule`
- Lines: 187-187
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### reference-semantics/semantics/builtins.k:188:ac5c7747453b

- Kind: `syntax`
- Lines: 188-188
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### reference-semantics/semantics/builtins.k:189:05258192fa0b

- Kind: `rule`
- Lines: 189-190
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### reference-semantics/semantics/builtins.k:192:82f289aff157

- Kind: `syntax`
- Lines: 192-192
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### reference-semantics/semantics/builtins.k:194:b174a010e1cc

- Kind: `syntax`
- Lines: 194-194
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### reference-semantics/semantics/builtins.k:195:3e38e9b3918a

- Kind: `rule`
- Lines: 195-195
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### reference-semantics/semantics/builtins.k:196:7322fabc33c9

- Kind: `syntax`
- Lines: 196-196
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:197:8943c2a4d630

- Kind: `rule`
- Lines: 197-197
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### reference-semantics/semantics/builtins.k:198:ef5ec403ed14

- Kind: `rule`
- Lines: 198-198
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### reference-semantics/semantics/builtins.k:199:0c7954767f99

- Kind: `syntax`
- Lines: 199-199
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:200:238e1f40d90a

- Kind: `rule`
- Lines: 200-200
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### reference-semantics/semantics/builtins.k:201:04deaa8cfac7

- Kind: `rule`
- Lines: 201-201
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### reference-semantics/semantics/builtins.k:203:d6d582239dd5

- Kind: `syntax`
- Lines: 203-203
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:204:cad0dda355df

- Kind: `rule`
- Lines: 204-204
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### reference-semantics/semantics/builtins.k:205:ac016e542b18

- Kind: `rule`
- Lines: 205-205
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### reference-semantics/semantics/builtins.k:206:aeb40dc57a6a

- Kind: `rule`
- Lines: 206-206
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### reference-semantics/semantics/builtins.k:207:011c9edcd2e8

- Kind: `rule`
- Lines: 207-207
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### reference-semantics/semantics/builtins.k:208:884a4ea6adfc

- Kind: `rule`
- Lines: 208-208
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### reference-semantics/semantics/builtins.k:209:005eaf8a7dd6

- Kind: `rule`
- Lines: 209-209
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### reference-semantics/semantics/builtins.k:210:edd2b8a2a065

- Kind: `rule`
- Lines: 210-210
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### reference-semantics/semantics/builtins.k:211:f7ba86c9174e

- Kind: `rule`
- Lines: 211-211
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### reference-semantics/semantics/builtins.k:212:bb5f349b145f

- Kind: `rule`
- Lines: 212-212
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### reference-semantics/semantics/builtins.k:214:996ffada5296

- Kind: `syntax`
- Lines: 214-215
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:216:4254b9f7b231

- Kind: `rule`
- Lines: 216-216
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### reference-semantics/semantics/builtins.k:217:1f722e6081e1

- Kind: `rule`
- Lines: 217-217
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### reference-semantics/semantics/builtins.k:218:2378510f6563

- Kind: `rule`
- Lines: 218-218
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### reference-semantics/semantics/builtins.k:219:50035ba8e969

- Kind: `rule`
- Lines: 219-220
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### reference-semantics/semantics/builtins.k:221:84ee76f78e14

- Kind: `rule`
- Lines: 221-222
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### reference-semantics/semantics/builtins.k:223:a5f697b9adb7

- Kind: `rule`
- Lines: 223-223
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### reference-semantics/semantics/builtins.k:225:906d0c17f2fb

- Kind: `syntax`
- Lines: 225-225
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### reference-semantics/semantics/builtins.k:226:cdf7f8b500cf

- Kind: `syntax`
- Lines: 226-226
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:227:493a0efa8ace

- Kind: `rule`
- Lines: 227-227
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### reference-semantics/semantics/builtins.k:228:99460cf0fcab

- Kind: `rule`
- Lines: 228-228
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### reference-semantics/semantics/builtins.k:230:f15a46d2a884

- Kind: `syntax`
- Lines: 230-230
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:231:f63fbddd4228

- Kind: `rule`
- Lines: 231-231
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### reference-semantics/semantics/builtins.k:232:f3a95c1d102c

- Kind: `rule`
- Lines: 232-232
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### reference-semantics/semantics/builtins.k:233:83add421a531

- Kind: `rule`
- Lines: 233-233
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### reference-semantics/semantics/builtins.k:234:fe469f129f99

- Kind: `rule`
- Lines: 234-234
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### reference-semantics/semantics/builtins.k:235:45890407b049

- Kind: `rule`
- Lines: 235-235
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### reference-semantics/semantics/builtins.k:236:77542379cedb

- Kind: `rule`
- Lines: 236-236
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### reference-semantics/semantics/builtins.k:238:7039540535a2

- Kind: `syntax`
- Lines: 238-238
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:239:337779ec3207

- Kind: `rule`
- Lines: 239-239
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### reference-semantics/semantics/builtins.k:240:cfc7aaf38685

- Kind: `rule`
- Lines: 240-240
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### reference-semantics/semantics/builtins.k:241:ebdd09e2ea67

- Kind: `rule`
- Lines: 241-242
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### reference-semantics/semantics/builtins.k:243:25a4663fe177

- Kind: `rule`
- Lines: 243-243
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### reference-semantics/semantics/builtins.k:244:6a975303e128

- Kind: `syntax`
- Lines: 244-244
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:245:b0fe3350706d

- Kind: `rule`
- Lines: 245-245
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### reference-semantics/semantics/builtins.k:246:2474e1e106b7

- Kind: `rule`
- Lines: 246-246
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### reference-semantics/semantics/builtins.k:247:ccb2ec4ebb2f

- Kind: `syntax`
- Lines: 247-247
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:248:1b1d231b33e5

- Kind: `rule`
- Lines: 248-248
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### reference-semantics/semantics/builtins.k:250:b236e49f85be

- Kind: `syntax`
- Lines: 250-250
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:251:e5919eeb7c7e

- Kind: `rule`
- Lines: 251-251
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### reference-semantics/semantics/builtins.k:252:6b1d3c71e798

- Kind: `rule`
- Lines: 252-252
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### reference-semantics/semantics/builtins.k:253:c3f2a5ab71fe

- Kind: `rule`
- Lines: 253-253
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### reference-semantics/semantics/builtins.k:254:8842e532de29

- Kind: `rule`
- Lines: 254-254
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### reference-semantics/semantics/builtins.k:255:3b8c247c3782

- Kind: `syntax`
- Lines: 255-255
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:256:1232a86fdb86

- Kind: `rule`
- Lines: 256-256
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### reference-semantics/semantics/builtins.k:257:92900e548ab8

- Kind: `rule`
- Lines: 257-259
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### reference-semantics/semantics/builtins.k:260:c0996a5da68b

- Kind: `rule`
- Lines: 260-262
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### reference-semantics/semantics/builtins.k:263:25373bd79114

- Kind: `rule`
- Lines: 263-264
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### reference-semantics/semantics/builtins.k:265:241368398e21

- Kind: `syntax`
- Lines: 265-265
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### reference-semantics/semantics/builtins.k:266:55734e1ee045

- Kind: `rule`
- Lines: 266-266
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### reference-semantics/semantics/builtins.k:267:d4ca4934e9e1

- Kind: `rule`
- Lines: 267-267
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### reference-semantics/semantics/builtins.k:268:7c8e03ff739b

- Kind: `rule`
- Lines: 268-268
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### reference-semantics/semantics/builtins.k:269:b9870a621ad1

- Kind: `syntax`
- Lines: 269-269
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### reference-semantics/semantics/builtins.k:270:7a7e56f73880

- Kind: `rule`
- Lines: 270-270
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### reference-semantics/semantics/builtins.k:271:d0623558f5e8

- Kind: `rule`
- Lines: 271-271
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### reference-semantics/semantics/builtins.k:272:5895024c900e

- Kind: `syntax`
- Lines: 272-272
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:273:0a8e13361178

- Kind: `rule`
- Lines: 273-273
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### reference-semantics/semantics/builtins.k:274:2d4ab3afff7d

- Kind: `rule`
- Lines: 274-278
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### reference-semantics/semantics/builtins.k:279:daf634ba2a45

- Kind: `syntax`
- Lines: 279-279
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= "#md5"
```

### reference-semantics/semantics/builtins.k:280:90e43d1cdca9

- Kind: `rule`
- Lines: 280-281
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### reference-semantics/semantics/builtins.k:282:3dea3e5b7893

- Kind: `rule`
- Lines: 282-282
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### reference-semantics/semantics/builtins.k:283:697d07fdfb43

- Kind: `syntax`
- Lines: 283-283
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= md5Obj(IntSeq)
```

### reference-semantics/semantics/builtins.k:284:314edc78f759

- Kind: `rule`
- Lines: 284-284
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### reference-semantics/semantics/builtins.k:285:43bc3c3c9885

- Kind: `syntax`
- Lines: 285-290
- Attributes: `function`, `symbol(md5hexCodes)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### reference-semantics/semantics/builtins.k:291:89ae05ae7446

- Kind: `rule`
- Lines: 291-291
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### reference-semantics/semantics/builtins.k:292:42f642e09611

- Kind: `rule`
- Lines: 292-292
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### reference-semantics/semantics/builtins.k:293:09de746af4b8

- Kind: `syntax`
- Lines: 293-293
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### reference-semantics/semantics/builtins.k:294:2ac5e818e75e

- Kind: `rule`
- Lines: 294-294
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule isIntV(_:Int)         => true
```

### reference-semantics/semantics/builtins.k:295:f15a463d63cd

- Kind: `rule`
- Lines: 295-295
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule isIntV(_:Val)         => false [owise]
```

### reference-semantics/semantics/builtins.k:296:d3c0ce1552b2

- Kind: `rule`
- Lines: 296-296
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule isStrV(str(_:IntSeq)) => true
```

### reference-semantics/semantics/builtins.k:297:2615ec2618f0

- Kind: `rule`
- Lines: 297-297
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule isStrV(_:Val)         => false [owise]
```

### reference-semantics/semantics/builtins.k:298:4c5df27adc71

- Kind: `endmodule`
- Lines: 298-298
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/call.k:10:876a0ba2b4a1

- Kind: `module`
- Lines: 10-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-CALL
```

### reference-semantics/semantics/call.k:11:09fe9e0706ae

- Kind: `imports`
- Lines: 11-11
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-METHODS
```

### reference-semantics/semantics/call.k:12:513b07985ad1

- Kind: `imports`
- Lines: 12-12
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-BUILTINS
```

### reference-semantics/semantics/call.k:13:847aa9d4d4c0

- Kind: `imports`
- Lines: 13-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-FUNCTIONS

  // a cooled attribute is a bound method value
```

### reference-semantics/semantics/call.k:16:24066eeea708

- Kind: `rule`
- Lines: 16-18
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### reference-semantics/semantics/call.k:19:2e4b9931b31d

- Kind: `syntax`
- Lines: 19-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #callee(Exprs)
```

### reference-semantics/semantics/call.k:20:1e7cf6c3f022

- Kind: `rule`
- Lines: 20-20
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### reference-semantics/semantics/call.k:21:a17200963b4c

- Kind: `rule`
- Lines: 21-23
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### reference-semantics/semantics/call.k:24:ba0da2a7daa0

- Kind: `rule`
- Lines: 24-24
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### reference-semantics/semantics/call.k:26:9355577d2cbe

- Kind: `rule`
- Lines: 26-26
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### reference-semantics/semantics/call.k:27:3025de857057

- Kind: `rule`
- Lines: 27-27
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### reference-semantics/semantics/call.k:28:1037499b709e

- Kind: `rule`
- Lines: 28-28
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### reference-semantics/semantics/call.k:29:02fe785764c6

- Kind: `rule`
- Lines: 29-29
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### reference-semantics/semantics/call.k:30:74e89a0d00ed

- Kind: `rule`
- Lines: 30-30
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### reference-semantics/semantics/call.k:31:6240ee6cdac4

- Kind: `rule`
- Lines: 31-31
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### reference-semantics/semantics/call.k:32:c54245698f6b

- Kind: `rule`
- Lines: 32-37
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### reference-semantics/semantics/call.k:38:ec48bd542daf

- Kind: `rule`
- Lines: 38-41
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/call.k:42:fb1cf54c5dbf

- Kind: `rule`
- Lines: 42-46
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### reference-semantics/semantics/call.k:47:a9d4dc84230b

- Kind: `rule`
- Lines: 47-50
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/call.k:52:d5c2626ac8a7

- Kind: `syntax`
- Lines: 52-52
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### reference-semantics/semantics/call.k:53:a17ba7979cef

- Kind: `rule`
- Lines: 53-55
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### reference-semantics/semantics/call.k:56:3507960157a5

- Kind: `rule`
- Lines: 56-62
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
  // non-mutating methods READ their heap-object arguments too (join's list);
  // mutators keep refs (append of a list into a list-of-lists stays aliased)
```

### reference-semantics/semantics/call.k:63:09356ec82fd2

- Kind: `rule`
- Lines: 63-67
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### reference-semantics/semantics/call.k:69:b6441b147406

- Kind: `rule`
- Lines: 69-79
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>

  // annotated closure: the frame starts with the captured freevar cells, its
  // parent is the module scope (all enclosing-local reads go through cells),
  // and the cellvars' fresh cells allocate before params bind (a cellvar param
  // then writes through its cell in #bindP).
```

### reference-semantics/semantics/call.k:80:7306d2306298

- Kind: `rule`
- Lines: 80-85
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### reference-semantics/semantics/call.k:87:66b816d7dbbc

- Kind: `syntax`
- Lines: 87-87
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### reference-semantics/semantics/call.k:88:ab5f4beee335

- Kind: `rule`
- Lines: 88-88
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### reference-semantics/semantics/call.k:89:99f0ab53a196

- Kind: `rule`
- Lines: 89-94
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### reference-semantics/semantics/call.k:95:4c5df27adc71

- Kind: `endmodule`
- Lines: 95-95
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/comprehension.k:3:5d080156bedb

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-COMPREHENSION
```

### reference-semantics/semantics/comprehension.k:4:4258a966960e

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/comprehension.k:5:ee018db6efb0

- Kind: `imports`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-OPERATORS
```

### reference-semantics/semantics/comprehension.k:6:511c798e04e9

- Kind: `imports`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-LIST
```

### reference-semantics/semantics/comprehension.k:7:47dfd92e317b

- Kind: `imports`
- Lines: 7-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CONTROLS
```

### reference-semantics/semantics/comprehension.k:8:e7f30157a500

- Kind: `imports`
- Lines: 8-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-FUNCTIONS

  // A comprehension is pure syntactic sugar
```

### reference-semantics/semantics/comprehension.k:11:4645372e277c

- Kind: `rule`
- Lines: 11-11
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### reference-semantics/semantics/comprehension.k:12:dfe1627b5b2d

- Kind: `rule`
- Lines: 12-12
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### reference-semantics/semantics/comprehension.k:14:824d607beedb

- Kind: `syntax`
- Lines: 14-14
- Attributes: `macro`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### reference-semantics/semantics/comprehension.k:15:815fb636c44d

- Kind: `rule`
- Lines: 15-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### reference-semantics/semantics/comprehension.k:18:7d588d134f4b

- Kind: `syntax`
- Lines: 18-18
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### reference-semantics/semantics/comprehension.k:19:03f45d480d0d

- Kind: `rule`
- Lines: 19-20
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### reference-semantics/semantics/comprehension.k:21:671328ad859b

- Kind: `rule`
- Lines: 21-22
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### reference-semantics/semantics/comprehension.k:24:2ecdbee509dd

- Kind: `syntax`
- Lines: 24-24
- Attributes: `macro`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### reference-semantics/semantics/comprehension.k:25:7be24aff205f

- Kind: `rule`
- Lines: 25-25
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### reference-semantics/semantics/comprehension.k:26:93505f664b89

- Kind: `rule`
- Lines: 26-26
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### reference-semantics/semantics/comprehension.k:27:4c5df27adc71

- Kind: `endmodule`
- Lines: 27-27
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/concrete.k:8:31e028e78e3c

- Kind: `module`
- Lines: 8-8
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
module MPY-CONCRETE
```

### reference-semantics/semantics/concrete.k:9:c632734fb5a0

- Kind: `imports`
- Lines: 9-12
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  imports MPY

  // deep equality for list compares whose elements are heap objects
  // (list-of-lists): Python == is structural at every depth.
```

### reference-semantics/semantics/concrete.k:13:78076bacc787

- Kind: `rule`
- Lines: 13-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### reference-semantics/semantics/concrete.k:16:ee70f13486ee

- Kind: `rule`
- Lines: 16-24
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)

  // ==== keyed sort, concrete leg ============================================
  // Computes each key by a REAL call through the uniform #callee machinery
  // (closures, len, type objects all work), stable-inserts on the key, and
  // allocates the result. priority(40) beats sort.k's opaque rules, so krun
  // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.
```

### reference-semantics/semantics/concrete.k:25:2a9016918418

- Kind: `syntax`
- Lines: 25-25
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  syntax Val ::= kvP(Val, Val)
```

### reference-semantics/semantics/concrete.k:26:1123d008aaa0

- Kind: `syntax`
- Lines: 26-27
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### reference-semantics/semantics/concrete.k:28:5caca2001b70

- Kind: `rule`
- Lines: 28-30
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/concrete.k:31:2c4b50fac01d

- Kind: `rule`
- Lines: 31-33
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/concrete.k:34:9a2cac297472

- Kind: `rule`
- Lines: 34-35
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### reference-semantics/semantics/concrete.k:36:1b960e24430b

- Kind: `rule`
- Lines: 36-37
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### reference-semantics/semantics/concrete.k:38:833a30eb0045

- Kind: `rule`
- Lines: 38-40
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### reference-semantics/semantics/concrete.k:42:55dc07274299

- Kind: `syntax`
- Lines: 42-42
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### reference-semantics/semantics/concrete.k:43:1b9c47e83939

- Kind: `rule`
- Lines: 43-43
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### reference-semantics/semantics/concrete.k:44:111715f3eff9

- Kind: `rule`
- Lines: 44-46
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### reference-semantics/semantics/concrete.k:47:b54f5a2a0368

- Kind: `rule`
- Lines: 47-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### reference-semantics/semantics/concrete.k:51:a74ccb7aaf4f

- Kind: `syntax`
- Lines: 51-51
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### reference-semantics/semantics/concrete.k:52:2123b754255b

- Kind: `rule`
- Lines: 52-52
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### reference-semantics/semantics/concrete.k:53:fa99ec9f191b

- Kind: `rule`
- Lines: 53-53
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### reference-semantics/semantics/concrete.k:54:608ffd1665ed

- Kind: `rule`
- Lines: 54-54
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### reference-semantics/semantics/concrete.k:56:4f9bc29fa28a

- Kind: `syntax`
- Lines: 56-56
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### reference-semantics/semantics/concrete.k:57:a2e6dd066c67

- Kind: `rule`
- Lines: 57-57
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### reference-semantics/semantics/concrete.k:58:84d1ae0473a1

- Kind: `rule`
- Lines: 58-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### reference-semantics/semantics/concrete.k:59:7ae54fdad398

- Kind: `rule`
- Lines: 59-59
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### reference-semantics/semantics/concrete.k:60:4c5df27adc71

- Kind: `endmodule`
- Lines: 60-60
- Attributes: none
- Decision: `FIXED_SUPPLIED_CONCRETE_ONLY`
- Rationale: Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.

```k
endmodule
```

### reference-semantics/semantics/controls.k:3:f64b2208f5bd

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-CONTROLS
```

### reference-semantics/semantics/controls.k:4:4258a966960e

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/controls.k:5:b1d1ddeb005d

- Kind: `imports`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-TUPLE
```

### reference-semantics/semantics/controls.k:6:b578ab301681

- Kind: `imports`
- Lines: 6-8
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-ITER

  // ==== Assign / AugAssign (write the current scope; RHS evaluated by strictness) ==
```

### reference-semantics/semantics/controls.k:9:a78b31a11fb1

- Kind: `rule`
- Lines: 9-11
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### reference-semantics/semantics/controls.k:12:46fcacaf0429

- Kind: `rule`
- Lines: 12-18
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### reference-semantics/semantics/controls.k:20:86c0c2c41772

- Kind: `rule`
- Lines: 20-26
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
  // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
  // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
  // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
```

### reference-semantics/semantics/controls.k:27:48037c0fb312

- Kind: `rule`
- Lines: 27-34
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]

  // ==== import trivia: `from math import floor, ceil` binds the supported
  // names as builtins in the current scope; every other import is a no-op
```

### reference-semantics/semantics/controls.k:35:f402a7269397

- Kind: `rule`
- Lines: 35-35
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### reference-semantics/semantics/controls.k:36:52700f6597b2

- Kind: `rule`
- Lines: 36-36
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### reference-semantics/semantics/controls.k:37:88b5590c6cf0

- Kind: `syntax`
- Lines: 37-37
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### reference-semantics/semantics/controls.k:38:775670eae46f

- Kind: `rule`
- Lines: 38-38
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### reference-semantics/semantics/controls.k:39:16792e79fae5

- Kind: `rule`
- Lines: 39-42
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### reference-semantics/semantics/controls.k:43:149ac3587bf6

- Kind: `rule`
- Lines: 43-47
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

### reference-semantics/semantics/controls.k:48:6e525bc694fa

- Kind: `rule`
- Lines: 48-50
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### reference-semantics/semantics/controls.k:51:7b0fe50a6219

- Kind: `syntax`
- Lines: 51-51
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### reference-semantics/semantics/controls.k:52:cbe0a65ca8b4

- Kind: `rule`
- Lines: 52-52
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### reference-semantics/semantics/controls.k:53:590ba86f9c09

- Kind: `rule`
- Lines: 53-53
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### reference-semantics/semantics/controls.k:54:37fb93cd49df

- Kind: `rule`
- Lines: 54-56
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### reference-semantics/semantics/controls.k:57:7a11b92d5f39

- Kind: `rule`
- Lines: 57-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### reference-semantics/semantics/controls.k:59:769d03585768

- Kind: `rule`
- Lines: 59-64
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

### reference-semantics/semantics/controls.k:65:527ed693357c

- Kind: `syntax`
- Lines: 65-67
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### reference-semantics/semantics/controls.k:69:54e2c3c93eb9

- Kind: `rule`
- Lines: 69-69
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### reference-semantics/semantics/controls.k:71:f6431203e70c

- Kind: `rule`
- Lines: 71-71
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### reference-semantics/semantics/controls.k:72:e22f89d510cf

- Kind: `rule`
- Lines: 72-72
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### reference-semantics/semantics/controls.k:73:a1af2eb81632

- Kind: `rule`
- Lines: 73-76
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### reference-semantics/semantics/controls.k:77:cc778d0a7dee

- Kind: `rule`
- Lines: 77-77
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### reference-semantics/semantics/controls.k:78:6b4a239ea016

- Kind: `rule`
- Lines: 78-78
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### reference-semantics/semantics/controls.k:79:7954a0aef082

- Kind: `rule`
- Lines: 79-80
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### reference-semantics/semantics/controls.k:81:df659ad8351c

- Kind: `rule`
- Lines: 81-84
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

### reference-semantics/semantics/controls.k:85:bb87d59b209a

- Kind: `rule`
- Lines: 85-85
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### reference-semantics/semantics/controls.k:86:7987cb734506

- Kind: `rule`
- Lines: 86-86
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Continue => #cont ... </k>
```

### reference-semantics/semantics/controls.k:87:0c6690a88f1d

- Kind: `rule`
- Lines: 87-87
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Break => #brk ... </k>
```

### reference-semantics/semantics/controls.k:88:8617466b0146

- Kind: `rule`
- Lines: 88-88
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### reference-semantics/semantics/controls.k:89:5cabf37fa715

- Kind: `rule`
- Lines: 89-89
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### reference-semantics/semantics/controls.k:90:5b9a5f06df03

- Kind: `rule`
- Lines: 90-90
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### reference-semantics/semantics/controls.k:91:dfd7f5ed393c

- Kind: `rule`
- Lines: 91-94
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### reference-semantics/semantics/controls.k:95:ff65bd7ea83d

- Kind: `rule`
- Lines: 95-97
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/controls.k:98:a42c32523449

- Kind: `rule`
- Lines: 98-100
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/controls.k:101:da33a9064f83

- Kind: `rule`
- Lines: 101-105
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### reference-semantics/semantics/controls.k:106:32f13b8026fc

- Kind: `rule`
- Lines: 106-108
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/controls.k:109:4c5df27adc71

- Kind: `endmodule`
- Lines: 109-109
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/core.k:3:6f8de5b25360

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-CORE
```

### reference-semantics/semantics/core.k:4:53e3bff8f927

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-SYNTAX
```

### reference-semantics/semantics/core.k:5:e6c6a545c82f

- Kind: `imports`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports INT
```

### reference-semantics/semantics/core.k:6:a87b57b80409

- Kind: `imports`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports BOOL
```

### reference-semantics/semantics/core.k:7:0285d3d5d999

- Kind: `imports`
- Lines: 7-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports STRING
```

### reference-semantics/semantics/core.k:8:acf7e2a94c16

- Kind: `imports`
- Lines: 8-8
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MAP
```

### reference-semantics/semantics/core.k:9:82a7d762e104

- Kind: `imports`
- Lines: 9-9
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports LIST
```

### reference-semantics/semantics/core.k:10:4b342623be24

- Kind: `imports`
- Lines: 10-12
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports K-EQUAL

  // ==== values, the algebraic lists, and the scope heap =====================
```

### reference-semantics/semantics/core.k:13:2768b2d6c3a1

- Kind: `syntax`
- Lines: 13-13
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### reference-semantics/semantics/core.k:14:3571b0fa24f6

- Kind: `syntax`
- Lines: 14-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### reference-semantics/semantics/core.k:15:23461c6dc66d

- Kind: `syntax`
- Lines: 15-17
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### reference-semantics/semantics/core.k:18:2b8233305aea

- Kind: `syntax`
- Lines: 18-23
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### reference-semantics/semantics/core.k:25:f0009a449e07

- Kind: `syntax`
- Lines: 25-34
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Val      ::= Int
                    | Bool
                    | "noneV"
                    | Iterable
                    | ref(Int)          // a heap object: <heap> holds its list(VS)
                    | cellRef(Int)      // a closure cell: <heap> holds cellV(V)
                    | closureVal(ParamNames, Stmts, Int)
                    | typeV(String)     // a type object (int/str), resolved from the builtins frame
                    | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough)
                    | boundMethodV(Val, String)   // a cooled Attribute: obj.method
```

### reference-semantics/semantics/core.k:36:c240ca8787f6

- Kind: `syntax`
- Lines: 36-36
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Parent   ::= "root" | parent(Int)
```

### reference-semantics/semantics/core.k:37:1a4b85e2b644

- Kind: `syntax`
- Lines: 37-37
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Scope    ::= scope(Map, Parent)
```

### reference-semantics/semantics/core.k:38:190af4b16650

- Kind: `syntax`
- Lines: 38-38
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KResult  ::= Val
```

### reference-semantics/semantics/core.k:39:9dbbc23d4d9f

- Kind: `syntax`
- Lines: 39-39
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### reference-semantics/semantics/core.k:40:c9cee1981af7

- Kind: `syntax`
- Lines: 40-40
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Vals     ::= List{Val, ","}
```

### reference-semantics/semantics/core.k:41:1a9977b68187

- Kind: `syntax`
- Lines: 41-41
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### reference-semantics/semantics/core.k:42:4112a1e4d88e

- Kind: `syntax`
- Lines: 42-48
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### reference-semantics/semantics/core.k:49:1e728104ed09

- Kind: `configuration`
- Lines: 49-67
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  configuration
    <k>       #loadAll($PGM:Module) </k>
    <env>     0 </env>
    <scopes>   0     |-> scope(.Map, parent(-1))
              -1    |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>    .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>   .List </stack>
    <ret>     noRet </ret>
    <exc>     NoExc </exc>
    <exit-code exit=""> 0 </exit-code>

  // ==== heap allocation (constructed lists become objects) ==================
  // Cons-form emission with a freshness guard (the heap-list-probe discipline:
  // an update-form H[N <- _] never re-normalizes symbolically). heapLoc is
  // monotonic — it does NOT wind back at #pop: returned lists escape by ref.
  // A bare list(VS) Val stays legal (read-only inputs in claims flow unboxed);
  // only CONSTRUCTORS in program syntax allocate.
```

### reference-semantics/semantics/core.k:68:3338ad77ca00

- Kind: `syntax`
- Lines: 68-68
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### reference-semantics/semantics/core.k:69:d1ee5822bc20

- Kind: `rule`
- Lines: 69-69
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule isRefV(ref(_:Int)) => true
```

### reference-semantics/semantics/core.k:70:4a220c884823

- Kind: `rule`
- Lines: 70-74
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### reference-semantics/semantics/core.k:75:21cd98225d72

- Kind: `syntax`
- Lines: 75-75
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax HeapVal ::= cellV(Val)
```

### reference-semantics/semantics/core.k:76:a9d42f86eb00

- Kind: `syntax`
- Lines: 76-76
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### reference-semantics/semantics/core.k:77:d10f04444db1

- Kind: `rule`
- Lines: 77-77
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### reference-semantics/semantics/core.k:78:bfc7d2c0e8b4

- Kind: `rule`
- Lines: 78-84
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

### reference-semantics/semantics/core.k:85:f419fb039d2c

- Kind: `rule`
- Lines: 85-94
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]

  // write through a cell (Assign / #bindP / #bindTgt dispatch here on
  // cell-bound names)
  // a keyword argument cools to a TAGGED value (consumed by kw-aware builtins)
```

### reference-semantics/semantics/core.k:95:746e63785a2a

- Kind: `syntax`
- Lines: 95-95
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Val ::= kwV(String, Val)
```

### reference-semantics/semantics/core.k:96:7135e0a28684

- Kind: `syntax`
- Lines: 96-96
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #kwTag(String)
```

### reference-semantics/semantics/core.k:97:28d46dc1bd55

- Kind: `rule`
- Lines: 97-97
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### reference-semantics/semantics/core.k:98:b16faf57f0a4

- Kind: `rule`
- Lines: 98-99
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### reference-semantics/semantics/core.k:100:50eabe9c99f3

- Kind: `syntax`
- Lines: 100-100
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### reference-semantics/semantics/core.k:101:a1fa116710bd

- Kind: `rule`
- Lines: 101-101
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### reference-semantics/semantics/core.k:102:ba3d029375b5

- Kind: `rule`
- Lines: 102-105
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### reference-semantics/semantics/core.k:106:2285105441dc

- Kind: `syntax`
- Lines: 106-106
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Val ::= cellsMark(ParamNames)
```

### reference-semantics/semantics/core.k:107:ad2441054e7f

- Kind: `syntax`
- Lines: 107-107
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### reference-semantics/semantics/core.k:108:dadd75df5321

- Kind: `rule`
- Lines: 108-108
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### reference-semantics/semantics/core.k:109:009b993788c2

- Kind: `syntax`
- Lines: 109-109
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### reference-semantics/semantics/core.k:110:09cb69784187

- Kind: `rule`
- Lines: 110-110
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule pnMember(_:String, .ParamNames) => false
```

### reference-semantics/semantics/core.k:111:40d3ebcbac2e

- Kind: `rule`
- Lines: 111-111
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### reference-semantics/semantics/core.k:113:16af91ae2538

- Kind: `syntax`
- Lines: 113-113
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #cellW(Val, Val)
```

### reference-semantics/semantics/core.k:114:8cd98c73610f

- Kind: `rule`
- Lines: 114-115
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### reference-semantics/semantics/core.k:117:584583182d33

- Kind: `syntax`
- Lines: 117-117
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #alloc(Val)
```

### reference-semantics/semantics/core.k:118:8ba6ee3da867

- Kind: `rule`
- Lines: 118-123
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

### reference-semantics/semantics/core.k:124:40d32b5e1ad1

- Kind: `syntax`
- Lines: 124-124
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #loadAll(Module)
```

### reference-semantics/semantics/core.k:125:831765b43e68

- Kind: `rule`
- Lines: 125-125
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### reference-semantics/semantics/core.k:126:622f8afd4910

- Kind: `rule`
- Lines: 126-126
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### reference-semantics/semantics/core.k:127:764b1a77381a

- Kind: `rule`
- Lines: 127-129
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### reference-semantics/semantics/core.k:130:68e17b99a979

- Kind: `syntax`
- Lines: 130-130
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #look(String, Int)
```

### reference-semantics/semantics/core.k:131:4dffd7efda70

- Kind: `rule`
- Lines: 131-131
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### reference-semantics/semantics/core.k:132:c128140bd355

- Kind: `rule`
- Lines: 132-144
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
  // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE
  // LOOKUP (higher priority beats the plain return above on concrete cell
  // bindings; abstract claim values take the plain rule unchanged) — this
  // covers cross-frame cell reads (a comprehension closure reading the
  // enclosing function's cellvar) without a narrowing-prone k-top redex
  // guarded on the FOUND frame's DECLARED cellvars (pnMember over the
  // cellsMark): decidable for every concrete frame pin — plain frames and
  // non-cell names prune outright, so an abstract looked-up value never
  // drags a narrowing cellV heap match along (probed on 5-intersperse and
  // Q4's abstract `numbers` in the annotated frame)
```

### reference-semantics/semantics/core.k:145:3b3293c98073

- Kind: `rule`
- Lines: 145-151
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### reference-semantics/semantics/core.k:152:37f50d6b2000

- Kind: `rule`
- Lines: 152-156
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

### reference-semantics/semantics/core.k:157:9b3d6c932d97

- Kind: `syntax`
- Lines: 157-157
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### reference-semantics/semantics/core.k:158:2feb2220c834

- Kind: `rule`
- Lines: 158-184
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule builtinsScope
    => scope(.Map [ "len"    <- builtinV("len")    ]
                  [ "set"    <- builtinV("set")    ]
                  [ "sum"    <- builtinV("sum")    ]
                  [ "abs"    <- builtinV("abs")    ]
                  [ "min"    <- builtinV("min")    ]
                  [ "max"    <- builtinV("max")    ]
                  [ "ord"    <- builtinV("ord")    ]
                  [ "chr"    <- builtinV("chr")    ]
                  [ "range"  <- builtinV("range")  ]
                  [ "all"    <- builtinV("all")    ]
                  [ "any"    <- builtinV("any")    ]
                  [ "zip"    <- builtinV("zip")    ]
                  [ "isinstance" <- builtinV("isinstance") ]
                  [ "sorted" <- builtinV("sorted") ]
                  [ "list"   <- builtinV("list")   ]
                  [ "round"  <- builtinV("round")  ]
                  [ "bin"    <- builtinV("bin")    ]
                  [ "enumerate" <- builtinV("enumerate") ]
                  [ "map"    <- builtinV("map")    ]
                  [ "eval"   <- builtinV("eval")   ]
                  [ "int"    <- typeV("int")       ]
                  [ "str"    <- typeV("str")       ]
                  [ "float"  <- typeV("float")     ], root)

  // ==== argument/element evaluation: ONE left-to-right loop, tagged by destination ==
  // (list/tuple literals and calls all use it; modules extend ApplyK with their tags)
```

### reference-semantics/semantics/core.k:185:0cd464bb92d6

- Kind: `syntax`
- Lines: 185-185
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax ApplyK ::= toCall(Val)
```

### reference-semantics/semantics/core.k:186:4c486ed4a149

- Kind: `syntax`
- Lines: 186-188
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### reference-semantics/semantics/core.k:189:e7135690e726

- Kind: `rule`
- Lines: 189-189
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### reference-semantics/semantics/core.k:190:aee090561fe2

- Kind: `rule`
- Lines: 190-190
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### reference-semantics/semantics/core.k:191:6cb56fbbec2e

- Kind: `rule`
- Lines: 191-193
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### reference-semantics/semantics/core.k:194:49f810c47c2d

- Kind: `rule`
- Lines: 194-194
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### reference-semantics/semantics/core.k:195:28c8aac589eb

- Kind: `rule`
- Lines: 195-195
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### reference-semantics/semantics/core.k:196:ce5d21d8ba4e

- Kind: `rule`
- Lines: 196-198
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### reference-semantics/semantics/core.k:199:c70b8b2eac36

- Kind: `syntax`
- Lines: 199-199
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bool ::= truthy(Val) [function]
```

### reference-semantics/semantics/core.k:200:6a5f897dddf5

- Kind: `rule`
- Lines: 200-200
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule truthy(B:Bool)          => B
```

### reference-semantics/semantics/core.k:201:ce79df9f62d4

- Kind: `rule`
- Lines: 201-201
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule truthy(noneV)           => false
```

### reference-semantics/semantics/core.k:202:028df8cf7244

- Kind: `rule`
- Lines: 202-202
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### reference-semantics/semantics/core.k:203:933b3fe9dcab

- Kind: `rule`
- Lines: 203-203
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### reference-semantics/semantics/core.k:204:75c0f2ab15c6

- Kind: `rule`
- Lines: 204-204
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### reference-semantics/semantics/core.k:205:c7afccb5eaf9

- Kind: `rule`
- Lines: 205-207
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### reference-semantics/semantics/core.k:208:01c72ea272fe

- Kind: `syntax`
- Lines: 208-208
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### reference-semantics/semantics/core.k:209:182a981e83f0

- Kind: `syntax`
- Lines: 209-209
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### reference-semantics/semantics/core.k:210:98b1c42dbd34

- Kind: `syntax`
- Lines: 210-212
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### reference-semantics/semantics/core.k:213:763cc5fd6e1a

- Kind: `syntax`
- Lines: 213-213
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### reference-semantics/semantics/core.k:214:60caff7a9f1f

- Kind: `rule`
- Lines: 214-214
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### reference-semantics/semantics/core.k:215:c67434450dfa

- Kind: `rule`
- Lines: 215-215
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### reference-semantics/semantics/core.k:217:7a97605e841a

- Kind: `syntax`
- Lines: 217-217
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### reference-semantics/semantics/core.k:218:702ecbf22fe6

- Kind: `rule`
- Lines: 218-218
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### reference-semantics/semantics/core.k:219:a18b7dd541ca

- Kind: `rule`
- Lines: 219-222
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### reference-semantics/semantics/core.k:223:dd74bc995871

- Kind: `syntax`
- Lines: 223-223
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### reference-semantics/semantics/core.k:224:04fc8b8adecf

- Kind: `rule`
- Lines: 224-224
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule vsLen(.ValSeq)                => 0
```

### reference-semantics/semantics/core.k:225:c1a7ece33229

- Kind: `rule`
- Lines: 225-225
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### reference-semantics/semantics/core.k:227:cefb7744efac

- Kind: `syntax`
- Lines: 227-227
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### reference-semantics/semantics/core.k:228:e4e059101c40

- Kind: `rule`
- Lines: 228-228
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule isLen(.IntSeq)                => 0
```

### reference-semantics/semantics/core.k:229:7246dff4d111

- Kind: `rule`
- Lines: 229-232
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### reference-semantics/semantics/core.k:233:912ccb9ff6dc

- Kind: `syntax`
- Lines: 233-233
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### reference-semantics/semantics/core.k:234:1ac12e956540

- Kind: `rule`
- Lines: 234-234
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### reference-semantics/semantics/core.k:235:cf509c2667ab

- Kind: `rule`
- Lines: 235-235
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### reference-semantics/semantics/core.k:236:5624986ca9eb

- Kind: `rule`
- Lines: 236-237
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### reference-semantics/semantics/core.k:238:db586ecb1b47

- Kind: `rule`
- Lines: 238-239
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### reference-semantics/semantics/core.k:240:4c5df27adc71

- Kind: `endmodule`
- Lines: 240-240
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/dict.k:13:d48a71acd507

- Kind: `module`
- Lines: 13-13
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-DICT
```

### reference-semantics/semantics/dict.k:14:4258a966960e

- Kind: `imports`
- Lines: 14-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/dict.k:15:8ad41781e06e

- Kind: `imports`
- Lines: 15-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-ITER
```

### reference-semantics/semantics/dict.k:16:09fe9e0706ae

- Kind: `imports`
- Lines: 16-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-METHODS
```

### reference-semantics/semantics/dict.k:17:be3866c50379

- Kind: `imports`
- Lines: 17-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-LIST

  // dict as PARALLEL ordered key/value ValSeqs (same length; keys distinct).
```

### reference-semantics/semantics/dict.k:20:8572b253b889

- Kind: `syntax`
- Lines: 20-22
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### reference-semantics/semantics/dict.k:23:30be194e1c62

- Kind: `syntax`
- Lines: 23-25
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### reference-semantics/semantics/dict.k:26:338fc50af3ec

- Kind: `rule`
- Lines: 26-26
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### reference-semantics/semantics/dict.k:27:f86750e273ef

- Kind: `rule`
- Lines: 27-27
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### reference-semantics/semantics/dict.k:28:d45ec799e4cd

- Kind: `rule`
- Lines: 28-29
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### reference-semantics/semantics/dict.k:30:b5cfd3165044

- Kind: `rule`
- Lines: 30-31
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### reference-semantics/semantics/dict.k:32:11cdf3974fe7

- Kind: `rule`
- Lines: 32-36
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### reference-semantics/semantics/dict.k:37:b1e4066d0d4a

- Kind: `syntax`
- Lines: 37-37
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### reference-semantics/semantics/dict.k:38:a5aab27421b2

- Kind: `rule`
- Lines: 38-38
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### reference-semantics/semantics/dict.k:39:140cbc9a1aee

- Kind: `rule`
- Lines: 39-39
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### reference-semantics/semantics/dict.k:40:6ebdf36eb9c6

- Kind: `rule`
- Lines: 40-42
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### reference-semantics/semantics/dict.k:43:97a166c788d6

- Kind: `syntax`
- Lines: 43-43
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### reference-semantics/semantics/dict.k:44:5164f3d147fc

- Kind: `rule`
- Lines: 44-44
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### reference-semantics/semantics/dict.k:45:a7de53160e02

- Kind: `rule`
- Lines: 45-48
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### reference-semantics/semantics/dict.k:49:a03444397cd8

- Kind: `syntax`
- Lines: 49-49
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### reference-semantics/semantics/dict.k:50:2527b32b669f

- Kind: `rule`
- Lines: 50-51
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### reference-semantics/semantics/dict.k:52:8b0c3eb1a71c

- Kind: `rule`
- Lines: 52-53
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### reference-semantics/semantics/dict.k:54:36cb9ab00f78

- Kind: `rule`
- Lines: 54-57
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### reference-semantics/semantics/dict.k:58:a13bf6a27f3a

- Kind: `rule`
- Lines: 58-62
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### reference-semantics/semantics/dict.k:63:2e626ca3a0e5

- Kind: `rule`
- Lines: 63-63
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### reference-semantics/semantics/dict.k:64:391e4efc5555

- Kind: `syntax`
- Lines: 64-64
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### reference-semantics/semantics/dict.k:65:970020bb4783

- Kind: `rule`
- Lines: 65-69
- Attributes: `priority(45)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### reference-semantics/semantics/dict.k:70:31f3f6e36c10

- Kind: `syntax`
- Lines: 70-70
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### reference-semantics/semantics/dict.k:71:1e5a897e737f

- Kind: `rule`
- Lines: 71-75
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### reference-semantics/semantics/dict.k:76:882d796d0a94

- Kind: `syntax`
- Lines: 76-76
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #dsetK(String, Val)
```

### reference-semantics/semantics/dict.k:77:4bbcefc7ea06

- Kind: `rule`
- Lines: 77-77
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### reference-semantics/semantics/dict.k:78:9d1ff995bd95

- Kind: `rule`
- Lines: 78-81
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### reference-semantics/semantics/dict.k:82:485423180bee

- Kind: `rule`
- Lines: 82-85
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### reference-semantics/semantics/dict.k:86:cfa9005e176e

- Kind: `syntax`
- Lines: 86-86
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### reference-semantics/semantics/dict.k:87:67e131e4b8b9

- Kind: `rule`
- Lines: 87-89
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### reference-semantics/semantics/dict.k:90:1c5323bfd95c

- Kind: `syntax`
- Lines: 90-90
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### reference-semantics/semantics/dict.k:91:458bf70556ac

- Kind: `rule`
- Lines: 91-91
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### reference-semantics/semantics/dict.k:92:d410771a907f

- Kind: `rule`
- Lines: 92-94
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### reference-semantics/semantics/dict.k:95:1c9db57ab415

- Kind: `rule`
- Lines: 95-96
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### reference-semantics/semantics/dict.k:97:24fc648b5bc5

- Kind: `syntax`
- Lines: 97-97
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### reference-semantics/semantics/dict.k:98:38e9c64805ad

- Kind: `rule`
- Lines: 98-98
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### reference-semantics/semantics/dict.k:99:cdfafd7d57f1

- Kind: `rule`
- Lines: 99-100
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### reference-semantics/semantics/dict.k:101:10fc860d42b9

- Kind: `syntax`
- Lines: 101-101
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### reference-semantics/semantics/dict.k:102:a145c44f31bf

- Kind: `rule`
- Lines: 102-102
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### reference-semantics/semantics/dict.k:103:6971aef40103

- Kind: `rule`
- Lines: 103-103
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### reference-semantics/semantics/dict.k:104:4c5df27adc71

- Kind: `endmodule`
- Lines: 104-104
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/float.k:14:987e02a6cef8

- Kind: `module`
- Lines: 14-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-FLOAT
```

### reference-semantics/semantics/float.k:15:ee018db6efb0

- Kind: `imports`
- Lines: 15-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-OPERATORS
```

### reference-semantics/semantics/float.k:16:513b07985ad1

- Kind: `imports`
- Lines: 16-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-BUILTINS
```

### reference-semantics/semantics/float.k:17:f55ad623e333

- Kind: `imports`
- Lines: 17-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports FLOAT

  // Float is a value; the float literal evaluates to the K Float.
```

### reference-semantics/semantics/float.k:20:f206c1a5ca92

- Kind: `syntax`
- Lines: 20-20
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= Float
```

### reference-semantics/semantics/float.k:21:b207a7493191

- Kind: `rule`
- Lines: 21-23
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### reference-semantics/semantics/float.k:24:f4862b43f760

- Kind: `syntax`
- Lines: 24-24
- Attributes: `function`, `symbol(intFloatDiv)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### reference-semantics/semantics/float.k:25:be877732fabb

- Kind: `rule`
- Lines: 25-25
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### reference-semantics/semantics/float.k:27:e94b3c7e6338

- Kind: `rule`
- Lines: 27-29
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### reference-semantics/semantics/float.k:30:3c7cef5fcc77

- Kind: `syntax`
- Lines: 30-30
- Attributes: `function`, `symbol(divII)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### reference-semantics/semantics/float.k:31:111c0e226da2

- Kind: `rule`
- Lines: 31-31
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:32:db8bc4510e9a

- Kind: `rule`
- Lines: 32-36
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### reference-semantics/semantics/float.k:37:26237ef2edca

- Kind: `syntax`
- Lines: 37-37
- Attributes: `function`, `symbol(floatMod)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### reference-semantics/semantics/float.k:38:f0f814d6f918

- Kind: `rule`
- Lines: 38-38
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### reference-semantics/semantics/float.k:39:56d4267f396e

- Kind: `rule`
- Lines: 39-42
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### reference-semantics/semantics/float.k:43:ce568cc9c8ae

- Kind: `rule`
- Lines: 43-43
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### reference-semantics/semantics/float.k:44:3b638863c6a6

- Kind: `rule`
- Lines: 44-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### reference-semantics/semantics/float.k:50:9675cd9c7a22

- Kind: `syntax`
- Lines: 50-50
- Attributes: `function`, `symbol(floatLt)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### reference-semantics/semantics/float.k:51:2a8121a4d91f

- Kind: `rule`
- Lines: 51-51
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### reference-semantics/semantics/float.k:52:c073d8cee697

- Kind: `rule`
- Lines: 52-52
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### reference-semantics/semantics/float.k:54:12a1faf44cdf

- Kind: `syntax`
- Lines: 54-54
- Attributes: `function`, `symbol(absF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### reference-semantics/semantics/float.k:55:b00b8066b8e9

- Kind: `rule`
- Lines: 55-55
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### reference-semantics/semantics/float.k:56:ac3fc3bb925b

- Kind: `rule`
- Lines: 56-60
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### reference-semantics/semantics/float.k:61:c333ce9ff143

- Kind: `rule`
- Lines: 61-64
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### reference-semantics/semantics/float.k:65:b46507b52502

- Kind: `syntax`
- Lines: 65-65
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= "#mathCeil"
```

### reference-semantics/semantics/float.k:66:6731784767d2

- Kind: `rule`
- Lines: 66-66
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:67:0e161c91ce8b

- Kind: `rule`
- Lines: 67-69
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### reference-semantics/semantics/float.k:70:7182dabba367

- Kind: `syntax`
- Lines: 70-70
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= "#mathFloor"
```

### reference-semantics/semantics/float.k:71:8c6ed970676f

- Kind: `rule`
- Lines: 71-71
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:72:65f0f3138bd4

- Kind: `rule`
- Lines: 72-72
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### reference-semantics/semantics/float.k:73:bb414e98ce7c

- Kind: `syntax`
- Lines: 73-73
- Attributes: `function`, `symbol(floorFI)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### reference-semantics/semantics/float.k:74:6f2278b445a3

- Kind: `rule`
- Lines: 74-74
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### reference-semantics/semantics/float.k:75:18ae1bc1eb50

- Kind: `rule`
- Lines: 75-77
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### reference-semantics/semantics/float.k:78:4f4ffc4a6628

- Kind: `rule`
- Lines: 78-78
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### reference-semantics/semantics/float.k:79:8c75b87dea7b

- Kind: `rule`
- Lines: 79-81
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### reference-semantics/semantics/float.k:82:533ce2092684

- Kind: `syntax`
- Lines: 82-82
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### reference-semantics/semantics/float.k:83:841a8e8cad16

- Kind: `rule`
- Lines: 83-83
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:84:fbcd9d035631

- Kind: `rule`
- Lines: 84-84
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### reference-semantics/semantics/float.k:85:f6ee2424cb4d

- Kind: `rule`
- Lines: 85-85
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### reference-semantics/semantics/float.k:86:5506be323911

- Kind: `syntax`
- Lines: 86-86
- Attributes: `function`, `symbol(toF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### reference-semantics/semantics/float.k:87:ed62a3a7f661

- Kind: `rule`
- Lines: 87-87
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule toF(F:Float) => F        [concrete]
```

### reference-semantics/semantics/float.k:88:f14e69883b5c

- Kind: `rule`
- Lines: 88-92
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### reference-semantics/semantics/float.k:93:526754603124

- Kind: `syntax`
- Lines: 93-93
- Attributes: `function`, `symbol(ceilF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### reference-semantics/semantics/float.k:94:c5ad02ae1641

- Kind: `rule`
- Lines: 94-94
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### reference-semantics/semantics/float.k:95:145b6bb5414a

- Kind: `rule`
- Lines: 95-98
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### reference-semantics/semantics/float.k:99:7d664b09c5b8

- Kind: `rule`
- Lines: 99-102
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### reference-semantics/semantics/float.k:103:bd9289f118f1

- Kind: `syntax`
- Lines: 103-103
- Attributes: `function`, `symbol(subF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### reference-semantics/semantics/float.k:104:12f60d082454

- Kind: `rule`
- Lines: 104-104
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### reference-semantics/semantics/float.k:105:600f864e0d4d

- Kind: `rule`
- Lines: 105-105
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### reference-semantics/semantics/float.k:107:91e03f2ac9cf

- Kind: `syntax`
- Lines: 107-107
- Attributes: `function`, `symbol(divF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### reference-semantics/semantics/float.k:108:26654b7bcf19

- Kind: `rule`
- Lines: 108-108
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### reference-semantics/semantics/float.k:109:ef46ce780b55

- Kind: `rule`
- Lines: 109-109
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### reference-semantics/semantics/float.k:111:2398531263a9

- Kind: `syntax`
- Lines: 111-111
- Attributes: `function`, `symbol(addF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### reference-semantics/semantics/float.k:112:3f45f3747744

- Kind: `rule`
- Lines: 112-112
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### reference-semantics/semantics/float.k:113:034cf2b77672

- Kind: `rule`
- Lines: 113-113
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### reference-semantics/semantics/float.k:115:4e0d8b299c85

- Kind: `syntax`
- Lines: 115-115
- Attributes: `function`, `symbol(mulF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### reference-semantics/semantics/float.k:116:46a5b95d90aa

- Kind: `rule`
- Lines: 116-116
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### reference-semantics/semantics/float.k:117:7bc5c419eaac

- Kind: `rule`
- Lines: 117-117
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### reference-semantics/semantics/float.k:119:47a046af374b

- Kind: `syntax`
- Lines: 119-119
- Attributes: `function`, `symbol(powF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### reference-semantics/semantics/float.k:120:88f0b7d20137

- Kind: `rule`
- Lines: 120-120
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### reference-semantics/semantics/float.k:121:8e212e6890f1

- Kind: `rule`
- Lines: 121-124
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### reference-semantics/semantics/float.k:125:9fdcc02ab4ee

- Kind: `syntax`
- Lines: 125-125
- Attributes: `function`, `symbol(gtF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### reference-semantics/semantics/float.k:126:088703ce3653

- Kind: `rule`
- Lines: 126-126
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### reference-semantics/semantics/float.k:127:0288d338940c

- Kind: `rule`
- Lines: 127-127
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### reference-semantics/semantics/float.k:128:5eb9299eb06c

- Kind: `rule`
- Lines: 128-128
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### reference-semantics/semantics/float.k:129:8450a60edb04

- Kind: `rule`
- Lines: 129-131
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### reference-semantics/semantics/float.k:132:f16ef18fbd1d

- Kind: `rule`
- Lines: 132-132
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### reference-semantics/semantics/float.k:133:6353492521ad

- Kind: `rule`
- Lines: 133-133
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### reference-semantics/semantics/float.k:134:7b68c3069735

- Kind: `rule`
- Lines: 134-134
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### reference-semantics/semantics/float.k:135:1409954604e5

- Kind: `rule`
- Lines: 135-135
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### reference-semantics/semantics/float.k:136:695a4d4bdd54

- Kind: `rule`
- Lines: 136-136
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### reference-semantics/semantics/float.k:137:8105c256a812

- Kind: `rule`
- Lines: 137-137
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### reference-semantics/semantics/float.k:138:74e2f8b58bc6

- Kind: `rule`
- Lines: 138-138
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### reference-semantics/semantics/float.k:139:e6ec45cad51d

- Kind: `rule`
- Lines: 139-141
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### reference-semantics/semantics/float.k:142:4d0d2ce425b4

- Kind: `syntax`
- Lines: 142-142
- Attributes: `function`, `symbol(eqF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### reference-semantics/semantics/float.k:143:9653dcd55b20

- Kind: `rule`
- Lines: 143-143
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### reference-semantics/semantics/float.k:144:ac77f892cfc0

- Kind: `rule`
- Lines: 144-144
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### reference-semantics/semantics/float.k:145:722beef5b388

- Kind: `rule`
- Lines: 145-145
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### reference-semantics/semantics/float.k:146:15bc1d1e3d08

- Kind: `rule`
- Lines: 146-146
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### reference-semantics/semantics/float.k:147:330ac8e38f2c

- Kind: `rule`
- Lines: 147-147
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### reference-semantics/semantics/float.k:148:1714c1550770

- Kind: `rule`
- Lines: 148-148
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### reference-semantics/semantics/float.k:149:a3b308b7b2c2

- Kind: `rule`
- Lines: 149-149
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### reference-semantics/semantics/float.k:150:fc6de3b7c2f9

- Kind: `rule`
- Lines: 150-150
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### reference-semantics/semantics/float.k:151:6be006c5f338

- Kind: `rule`
- Lines: 151-153
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### reference-semantics/semantics/float.k:154:ed4df68a2d97

- Kind: `rule`
- Lines: 154-154
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### reference-semantics/semantics/float.k:155:36ca091848db

- Kind: `rule`
- Lines: 155-159
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### reference-semantics/semantics/float.k:160:588f5768440e

- Kind: `syntax`
- Lines: 160-160
- Attributes: `function`, `symbol(decStrToF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### reference-semantics/semantics/float.k:161:32ad68f36a35

- Kind: `rule`
- Lines: 161-161
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### reference-semantics/semantics/float.k:162:9f3e9336e6d4

- Kind: `rule`
- Lines: 162-164
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### reference-semantics/semantics/float.k:165:7ccb5a6fa421

- Kind: `syntax`
- Lines: 165-165
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### reference-semantics/semantics/float.k:166:87f97131d232

- Kind: `rule`
- Lines: 166-166
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### reference-semantics/semantics/float.k:167:81addd4f5596

- Kind: `syntax`
- Lines: 167-167
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/float.k:168:8628f4bdac5b

- Kind: `rule`
- Lines: 168-168
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### reference-semantics/semantics/float.k:169:b0b8a3b71d8b

- Kind: `rule`
- Lines: 169-169
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### reference-semantics/semantics/float.k:170:afe4cef68f53

- Kind: `rule`
- Lines: 170-170
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### reference-semantics/semantics/float.k:171:449dadad749f

- Kind: `rule`
- Lines: 171-172
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### reference-semantics/semantics/float.k:173:89e3dfc58231

- Kind: `syntax`
- Lines: 173-173
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/float.k:174:63e7386de829

- Kind: `rule`
- Lines: 174-174
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fracPart(.IntSeq) => 0
```

### reference-semantics/semantics/float.k:175:336f8c20b7a9

- Kind: `rule`
- Lines: 175-175
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### reference-semantics/semantics/float.k:176:517a796c8a51

- Kind: `rule`
- Lines: 176-176
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### reference-semantics/semantics/float.k:177:3a7473c8713b

- Kind: `rule`
- Lines: 177-177
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### reference-semantics/semantics/float.k:178:a87341fff574

- Kind: `rule`
- Lines: 178-178
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### reference-semantics/semantics/float.k:179:dffc425acef9

- Kind: `syntax`
- Lines: 179-179
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/float.k:180:f006d2881246

- Kind: `rule`
- Lines: 180-180
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fracScale(.IntSeq) => 1
```

### reference-semantics/semantics/float.k:181:abcd00241d75

- Kind: `rule`
- Lines: 181-181
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### reference-semantics/semantics/float.k:182:abd5cc4adcbe

- Kind: `rule`
- Lines: 182-182
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### reference-semantics/semantics/float.k:183:1e74ce0b2611

- Kind: `rule`
- Lines: 183-183
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### reference-semantics/semantics/float.k:184:21eab0b39d56

- Kind: `rule`
- Lines: 184-184
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### reference-semantics/semantics/float.k:185:a528cb142102

- Kind: `rule`
- Lines: 185-185
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### reference-semantics/semantics/float.k:186:df11945a1b8f

- Kind: `rule`
- Lines: 186-186
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### reference-semantics/semantics/float.k:187:204a489bc7af

- Kind: `rule`
- Lines: 187-189
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### reference-semantics/semantics/float.k:190:f49cc043a05b

- Kind: `syntax`
- Lines: 190-190
- Attributes: `function`, `symbol(divFloatIntV)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### reference-semantics/semantics/float.k:191:a71c4a7b3d8c

- Kind: `rule`
- Lines: 191-191
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:192:49144daa1c72

- Kind: `rule`
- Lines: 192-194
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### reference-semantics/semantics/float.k:195:4f21c29912e1

- Kind: `syntax`
- Lines: 195-195
- Attributes: `function`, `symbol(intToF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### reference-semantics/semantics/float.k:196:389178d3dfd7

- Kind: `rule`
- Lines: 196-196
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:197:695a4d4bdd54

- Kind: `rule`
- Lines: 197-197
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### reference-semantics/semantics/float.k:198:8105c256a812

- Kind: `rule`
- Lines: 198-198
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### reference-semantics/semantics/float.k:199:7b68c3069735

- Kind: `rule`
- Lines: 199-199
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### reference-semantics/semantics/float.k:200:1409954604e5

- Kind: `rule`
- Lines: 200-200
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### reference-semantics/semantics/float.k:201:74e2f8b58bc6

- Kind: `rule`
- Lines: 201-201
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### reference-semantics/semantics/float.k:202:de611e1415d1

- Kind: `rule`
- Lines: 202-202
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### reference-semantics/semantics/float.k:203:1714c1550770

- Kind: `rule`
- Lines: 203-203
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### reference-semantics/semantics/float.k:204:a3b308b7b2c2

- Kind: `rule`
- Lines: 204-204
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### reference-semantics/semantics/float.k:205:fc6de3b7c2f9

- Kind: `rule`
- Lines: 205-205
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### reference-semantics/semantics/float.k:206:23764a6ef8f4

- Kind: `rule`
- Lines: 206-208
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### reference-semantics/semantics/float.k:209:11c17aa2d431

- Kind: `syntax`
- Lines: 209-209
- Attributes: `function`, `symbol(truncF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### reference-semantics/semantics/float.k:210:bee730d1e871

- Kind: `rule`
- Lines: 210-210
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### reference-semantics/semantics/float.k:211:651a7c3ee92f

- Kind: `rule`
- Lines: 211-211
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### reference-semantics/semantics/float.k:213:df11945a1b8f

- Kind: `rule`
- Lines: 213-213
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### reference-semantics/semantics/float.k:214:aedd7151045c

- Kind: `rule`
- Lines: 214-216
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### reference-semantics/semantics/float.k:217:d0b7f75c69f6

- Kind: `syntax`
- Lines: 217-217
- Attributes: `function`, `symbol(roundF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### reference-semantics/semantics/float.k:218:eb02485bbe26

- Kind: `rule`
- Lines: 218-222
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### reference-semantics/semantics/float.k:223:73ff3255d50d

- Kind: `syntax`
- Lines: 223-223
- Attributes: `function`, `symbol(roundFN)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### reference-semantics/semantics/float.k:224:2ae5db0795e6

- Kind: `rule`
- Lines: 224-226
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:227:196b869af070

- Kind: `rule`
- Lines: 227-227
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### reference-semantics/semantics/float.k:228:053cb084a542

- Kind: `rule`
- Lines: 228-228
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### reference-semantics/semantics/float.k:230:ccbc57547039

- Kind: `syntax`
- Lines: 230-230
- Attributes: `function`, `symbol(sqrtF)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### reference-semantics/semantics/float.k:231:6233ea5230d8

- Kind: `rule`
- Lines: 231-231
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### reference-semantics/semantics/float.k:232:cf723364ca5d

- Kind: `syntax`
- Lines: 232-232
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= "#mathSqrt"
```

### reference-semantics/semantics/float.k:233:9708f9876df9

- Kind: `rule`
- Lines: 233-233
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:234:7e79b6dbd8c0

- Kind: `rule`
- Lines: 234-234
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### reference-semantics/semantics/float.k:235:92aacf0f7d11

- Kind: `rule`
- Lines: 235-242
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

### reference-semantics/semantics/float.k:243:a63f310fdba5

- Kind: `syntax`
- Lines: 243-243
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### reference-semantics/semantics/float.k:244:838b90fdad47

- Kind: `rule`
- Lines: 244-244
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### reference-semantics/semantics/float.k:245:dfa99d6b3002

- Kind: `rule`
- Lines: 245-245
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### reference-semantics/semantics/float.k:246:35a797d2ae5f

- Kind: `rule`
- Lines: 246-246
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### reference-semantics/semantics/float.k:247:a1f41d00826c

- Kind: `rule`
- Lines: 247-248
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### reference-semantics/semantics/float.k:250:cd35b1a80916

- Kind: `syntax`
- Lines: 250-250
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### reference-semantics/semantics/float.k:251:785007e31d6e

- Kind: `rule`
- Lines: 251-251
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### reference-semantics/semantics/float.k:252:6b8405dae8d4

- Kind: `rule`
- Lines: 252-252
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### reference-semantics/semantics/float.k:253:700ae0c8579a

- Kind: `rule`
- Lines: 253-253
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### reference-semantics/semantics/float.k:254:8288a6943c5a

- Kind: `rule`
- Lines: 254-260
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

### reference-semantics/semantics/float.k:261:0abd52ddf475

- Kind: `syntax`
- Lines: 261-261
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### reference-semantics/semantics/float.k:262:2f1184f501b5

- Kind: `rule`
- Lines: 262-264
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### reference-semantics/semantics/float.k:265:65c1e01d9cd3

- Kind: `rule`
- Lines: 265-265
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### reference-semantics/semantics/float.k:266:a39fca22a153

- Kind: `rule`
- Lines: 266-266
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### reference-semantics/semantics/float.k:267:f1353b9a01f4

- Kind: `rule`
- Lines: 267-269
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### reference-semantics/semantics/float.k:270:dba3e0024842

- Kind: `rule`
- Lines: 270-272
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### reference-semantics/semantics/float.k:273:4c5df27adc71

- Kind: `endmodule`
- Lines: 273-273
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/functions.k:3:443014fc6330

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-FUNCTIONS
```

### reference-semantics/semantics/functions.k:4:3fde5b005137

- Kind: `imports`
- Lines: 4-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CORE

  // call routing + callee/arg evaluation (#callee/#args/#argCont) live in call.k;
  // this module owns the frame lifecycle (bind params, return, pop).
```

### reference-semantics/semantics/functions.k:8:38852cfad417

- Kind: `syntax`
- Lines: 8-13
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### reference-semantics/semantics/functions.k:14:f981471f7fe1

- Kind: `rule`
- Lines: 14-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### reference-semantics/semantics/functions.k:18:a6aeea98e7de

- Kind: `syntax`
- Lines: 18-18
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### reference-semantics/semantics/functions.k:19:a786c280fdd8

- Kind: `rule`
- Lines: 19-26
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

### reference-semantics/semantics/functions.k:27:3858d7c3acdf

- Kind: `syntax`
- Lines: 27-30
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### reference-semantics/semantics/functions.k:31:adf59ac49fac

- Kind: `syntax`
- Lines: 31-32
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### reference-semantics/semantics/functions.k:33:c7913840b3eb

- Kind: `rule`
- Lines: 33-35
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### reference-semantics/semantics/functions.k:36:9260d8509a74

- Kind: `rule`
- Lines: 36-41
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### reference-semantics/semantics/functions.k:42:79ce8ed09e91

- Kind: `rule`
- Lines: 42-45
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### reference-semantics/semantics/functions.k:47:deda77ab9351

- Kind: `rule`
- Lines: 47-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### reference-semantics/semantics/functions.k:50:37112d13ebff

- Kind: `rule`
- Lines: 50-52
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### reference-semantics/semantics/functions.k:53:ee95b3fb3c96

- Kind: `rule`
- Lines: 53-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### reference-semantics/semantics/functions.k:59:ef332e7b4b11

- Kind: `rule`
- Lines: 59-62
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### reference-semantics/semantics/functions.k:63:e3671d9bac62

- Kind: `rule`
- Lines: 63-63
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### reference-semantics/semantics/functions.k:64:6355110fbe62

- Kind: `rule`
- Lines: 64-67
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### reference-semantics/semantics/functions.k:68:609a54ad1ff7

- Kind: `rule`
- Lines: 68-77
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
        andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
       [priority(40)]

  // ==== return / pop the frame (the returned expr evaluates by strictness) ==
```

### reference-semantics/semantics/functions.k:78:e32ef37e336c

- Kind: `rule`
- Lines: 78-79
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### reference-semantics/semantics/functions.k:80:625259de2459

- Kind: `rule`
- Lines: 80-84
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### reference-semantics/semantics/functions.k:85:0976ba92bcac

- Kind: `rule`
- Lines: 85-90
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### reference-semantics/semantics/functions.k:91:4c5df27adc71

- Kind: `endmodule`
- Lines: 91-91
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/int.k:4:74fc45d7398a

- Kind: `module`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-INT
```

### reference-semantics/semantics/int.k:5:4258a966960e

- Kind: `imports`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/int.k:7:bea824a9d0c7

- Kind: `rule`
- Lines: 7-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### reference-semantics/semantics/int.k:9:c67b19f49aae

- Kind: `rule`
- Lines: 9-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### reference-semantics/semantics/int.k:11:515cc9110af9

- Kind: `rule`
- Lines: 11-11
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### reference-semantics/semantics/int.k:12:335d0401d429

- Kind: `rule`
- Lines: 12-12
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### reference-semantics/semantics/int.k:13:045a3b7ba0f8

- Kind: `rule`
- Lines: 13-13
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### reference-semantics/semantics/int.k:14:b25cf4d3a0b2

- Kind: `rule`
- Lines: 14-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### reference-semantics/semantics/int.k:15:7cfc166283c7

- Kind: `rule`
- Lines: 15-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### reference-semantics/semantics/int.k:16:85afa4d25d14

- Kind: `rule`
- Lines: 16-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### reference-semantics/semantics/int.k:17:614ae406522b

- Kind: `rule`
- Lines: 17-17
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### reference-semantics/semantics/int.k:19:c131b0a21233

- Kind: `syntax`
- Lines: 19-19
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### reference-semantics/semantics/int.k:20:e3bb9293bfde

- Kind: `rule`
- Lines: 20-20
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### reference-semantics/semantics/int.k:22:10360ae8affd

- Kind: `rule`
- Lines: 22-22
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### reference-semantics/semantics/int.k:23:c213716c432e

- Kind: `rule`
- Lines: 23-23
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### reference-semantics/semantics/int.k:24:fefdcde2267a

- Kind: `rule`
- Lines: 24-24
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### reference-semantics/semantics/int.k:25:463b1de8dd3e

- Kind: `rule`
- Lines: 25-25
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### reference-semantics/semantics/int.k:26:533193ddf05e

- Kind: `rule`
- Lines: 26-26
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### reference-semantics/semantics/int.k:27:14ecc12ef5ab

- Kind: `rule`
- Lines: 27-27
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### reference-semantics/semantics/int.k:28:4c5df27adc71

- Kind: `endmodule`
- Lines: 28-28
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/iter.k:6:65489422ea2a

- Kind: `module`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-ITER
```

### reference-semantics/semantics/iter.k:7:4258a966960e

- Kind: `imports`
- Lines: 7-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/iter.k:8:2fa814827c66

- Kind: `syntax`
- Lines: 8-8
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### reference-semantics/semantics/iter.k:9:4c5df27adc71

- Kind: `endmodule`
- Lines: 9-9
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/list.k:3:61efb165f96a

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-LIST
```

### reference-semantics/semantics/list.k:4:4258a966960e

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/list.k:5:8ad41781e06e

- Kind: `imports`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-ITER
```

### reference-semantics/semantics/list.k:6:30f0f78ff6f9

- Kind: `imports`
- Lines: 6-8
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-OPERATORS

  // ==== iteration (the iterator protocol's list case) =======================
```

### reference-semantics/semantics/list.k:9:92f64fe67070

- Kind: `rule`
- Lines: 9-9
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### reference-semantics/semantics/list.k:10:fdf21a976315

- Kind: `rule`
- Lines: 10-12
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### reference-semantics/semantics/list.k:13:3d024af826bb

- Kind: `syntax`
- Lines: 13-13
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax ApplyK ::= "toList"
```

### reference-semantics/semantics/list.k:14:f3163ec1febd

- Kind: `rule`
- Lines: 14-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### reference-semantics/semantics/list.k:15:68fcfe1bf720

- Kind: `rule`
- Lines: 15-17
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### reference-semantics/semantics/list.k:18:ac8c744da9bb

- Kind: `syntax`
- Lines: 18-18
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### reference-semantics/semantics/list.k:19:68f539c882c7

- Kind: `rule`
- Lines: 19-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### reference-semantics/semantics/list.k:20:7c426da56f88

- Kind: `rule`
- Lines: 20-23
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### reference-semantics/semantics/list.k:24:e435eea17b21

- Kind: `rule`
- Lines: 24-25
- Attributes: `priority(45)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### reference-semantics/semantics/list.k:27:408c1dfb03ff

- Kind: `rule`
- Lines: 27-27
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### reference-semantics/semantics/list.k:28:cf305df5136c

- Kind: `rule`
- Lines: 28-32
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### reference-semantics/semantics/list.k:33:afe83d38567e

- Kind: `syntax`
- Lines: 33-33
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### reference-semantics/semantics/list.k:34:49b8d0595610

- Kind: `rule`
- Lines: 34-34
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule hasRefVS(.ValSeq)                => false
```

### reference-semantics/semantics/list.k:35:3e47ea875f2d

- Kind: `rule`
- Lines: 35-35
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### reference-semantics/semantics/list.k:37:a77ca761dd61

- Kind: `syntax`
- Lines: 37-38
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### reference-semantics/semantics/list.k:39:d3fe72f99ea2

- Kind: `rule`
- Lines: 39-39
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### reference-semantics/semantics/list.k:40:c45656fdf64a

- Kind: `rule`
- Lines: 40-40
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### reference-semantics/semantics/list.k:41:f8711893a8fa

- Kind: `rule`
- Lines: 41-41
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### reference-semantics/semantics/list.k:42:75597ae93e20

- Kind: `rule`
- Lines: 42-43
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### reference-semantics/semantics/list.k:45:c5c0bdde4aba

- Kind: `rule`
- Lines: 45-46
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### reference-semantics/semantics/list.k:47:4eab3bce7e80

- Kind: `rule`
- Lines: 47-48
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### reference-semantics/semantics/list.k:49:3863900e8a58

- Kind: `rule`
- Lines: 49-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### reference-semantics/semantics/list.k:50:d0920aeb362d

- Kind: `rule`
- Lines: 50-52
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### reference-semantics/semantics/list.k:53:bef1266a523e

- Kind: `rule`
- Lines: 53-57
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### reference-semantics/semantics/list.k:58:e171041153df

- Kind: `syntax`
- Lines: 58-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### reference-semantics/semantics/list.k:59:816d231c73c9

- Kind: `rule`
- Lines: 59-59
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### reference-semantics/semantics/list.k:60:81419bc508ae

- Kind: `rule`
- Lines: 60-60
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### reference-semantics/semantics/list.k:61:e84f869d57a9

- Kind: `rule`
- Lines: 61-61
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### reference-semantics/semantics/list.k:62:d8442792286c

- Kind: `rule`
- Lines: 62-62
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### reference-semantics/semantics/list.k:63:65f8e4204476

- Kind: `rule`
- Lines: 63-64
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### reference-semantics/semantics/list.k:65:8b08b93c8199

- Kind: `rule`
- Lines: 65-66
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### reference-semantics/semantics/list.k:67:5511f8c4ec44

- Kind: `rule`
- Lines: 67-67
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### reference-semantics/semantics/list.k:68:4c5df27adc71

- Kind: `endmodule`
- Lines: 68-68
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/methods.k:3:47c4712939d7

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-METHODS
```

### reference-semantics/semantics/methods.k:4:4258a966960e

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/methods.k:5:5d664c02791d

- Kind: `imports`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports K-EQUAL
```

### reference-semantics/semantics/methods.k:6:1c022ad4e0c9

- Kind: `imports`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-STR
```

### reference-semantics/semantics/methods.k:7:acd494813fef

- Kind: `imports`
- Lines: 7-9
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-LIST

  // method-call routing + arg-eval live in call.k; this module owns applyMethod.
```

### reference-semantics/semantics/methods.k:10:04a7fbd0fd3f

- Kind: `syntax`
- Lines: 10-12
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### reference-semantics/semantics/methods.k:13:328b30a3774c

- Kind: `rule`
- Lines: 13-13
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### reference-semantics/semantics/methods.k:14:a6ae81f68d63

- Kind: `rule`
- Lines: 14-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### reference-semantics/semantics/methods.k:15:eb11f68e6087

- Kind: `rule`
- Lines: 15-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### reference-semantics/semantics/methods.k:16:79cee76b2983

- Kind: `rule`
- Lines: 16-18
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### reference-semantics/semantics/methods.k:19:d65f50abf047

- Kind: `rule`
- Lines: 19-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### reference-semantics/semantics/methods.k:20:1adc9077ccda

- Kind: `rule`
- Lines: 20-20
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### reference-semantics/semantics/methods.k:21:b905f221e7b8

- Kind: `rule`
- Lines: 21-25
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### reference-semantics/semantics/methods.k:26:7c16ae8ffba7

- Kind: `rule`
- Lines: 26-26
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### reference-semantics/semantics/methods.k:27:8449bace9b91

- Kind: `syntax`
- Lines: 27-27
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### reference-semantics/semantics/methods.k:28:dcb47502ba71

- Kind: `rule`
- Lines: 28-28
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:29:f2558775f8da

- Kind: `rule`
- Lines: 29-29
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### reference-semantics/semantics/methods.k:30:cd8b44612b02

- Kind: `rule`
- Lines: 30-33
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### reference-semantics/semantics/methods.k:34:21c9fe9f7420

- Kind: `rule`
- Lines: 34-34
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### reference-semantics/semantics/methods.k:35:277077c74e8e

- Kind: `syntax`
- Lines: 35-35
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### reference-semantics/semantics/methods.k:36:f4dfc7d2f461

- Kind: `rule`
- Lines: 36-36
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### reference-semantics/semantics/methods.k:37:17286b8b7ff9

- Kind: `rule`
- Lines: 37-38
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### reference-semantics/semantics/methods.k:39:0bf718afc195

- Kind: `rule`
- Lines: 39-40
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### reference-semantics/semantics/methods.k:41:121d0c58dbca

- Kind: `syntax`
- Lines: 41-41
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/methods.k:42:036bd013d44b

- Kind: `rule`
- Lines: 42-42
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### reference-semantics/semantics/methods.k:43:f7a542230356

- Kind: `rule`
- Lines: 43-43
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### reference-semantics/semantics/methods.k:44:751e61e19c1c

- Kind: `rule`
- Lines: 44-46
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### reference-semantics/semantics/methods.k:47:fc495b2dc6ff

- Kind: `rule`
- Lines: 47-47
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### reference-semantics/semantics/methods.k:48:4eeafed3826b

- Kind: `syntax`
- Lines: 48-48
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:49:4291267251ce

- Kind: `rule`
- Lines: 49-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:50:879a0736a8b4

- Kind: `rule`
- Lines: 50-50
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### reference-semantics/semantics/methods.k:51:988ee980274c

- Kind: `rule`
- Lines: 51-51
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### reference-semantics/semantics/methods.k:52:588afa88ddb7

- Kind: `syntax`
- Lines: 52-52
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:53:f72cb5914e4a

- Kind: `rule`
- Lines: 53-53
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### reference-semantics/semantics/methods.k:54:24b1a05b8e5d

- Kind: `rule`
- Lines: 54-54
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### reference-semantics/semantics/methods.k:55:51a4dff42e7f

- Kind: `rule`
- Lines: 55-57
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### reference-semantics/semantics/methods.k:58:63b34c278710

- Kind: `rule`
- Lines: 58-60
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### reference-semantics/semantics/methods.k:61:c96bc358fea5

- Kind: `rule`
- Lines: 61-63
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### reference-semantics/semantics/methods.k:64:bf346f893e63

- Kind: `rule`
- Lines: 64-64
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### reference-semantics/semantics/methods.k:65:b0bd756c2169

- Kind: `syntax`
- Lines: 65-65
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### reference-semantics/semantics/methods.k:66:99f68ecf56cf

- Kind: `rule`
- Lines: 66-66
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### reference-semantics/semantics/methods.k:67:87d9bfa2c6dc

- Kind: `rule`
- Lines: 67-67
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### reference-semantics/semantics/methods.k:68:2a3f9f97f1d5

- Kind: `rule`
- Lines: 68-71
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### reference-semantics/semantics/methods.k:72:3ffc01180f48

- Kind: `rule`
- Lines: 72-74
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/methods.k:75:a861b5acc26b

- Kind: `syntax`
- Lines: 75-75
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### reference-semantics/semantics/methods.k:76:e52130b97cee

- Kind: `rule`
- Lines: 76-76
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### reference-semantics/semantics/methods.k:77:c4024da56e0b

- Kind: `rule`
- Lines: 77-78
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### reference-semantics/semantics/methods.k:79:f1cc1f9753c6

- Kind: `rule`
- Lines: 79-81
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

### reference-semantics/semantics/methods.k:82:002dffc41af2

- Kind: `syntax`
- Lines: 82-82
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### reference-semantics/semantics/methods.k:83:7b979b52a546

- Kind: `rule`
- Lines: 83-83
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### reference-semantics/semantics/methods.k:84:0c970d4acf65

- Kind: `rule`
- Lines: 84-84
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### reference-semantics/semantics/methods.k:85:37f133bfa155

- Kind: `syntax`
- Lines: 85-85
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:86:f7b83fe95e9c

- Kind: `rule`
- Lines: 86-88
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### reference-semantics/semantics/methods.k:89:d2822bd51bea

- Kind: `rule`
- Lines: 89-93
- Attributes: `priority(39)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### reference-semantics/semantics/methods.k:94:01261c3f8fa4

- Kind: `rule`
- Lines: 94-96
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/methods.k:97:e3a030c4362d

- Kind: `syntax`
- Lines: 97-97
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### reference-semantics/semantics/methods.k:98:2d26406190b8

- Kind: `rule`
- Lines: 98-98
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### reference-semantics/semantics/methods.k:99:83564ea69e6a

- Kind: `rule`
- Lines: 99-100
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### reference-semantics/semantics/methods.k:101:73831c929787

- Kind: `rule`
- Lines: 101-102
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### reference-semantics/semantics/methods.k:104:83ed72ac9f08

- Kind: `rule`
- Lines: 104-105
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### reference-semantics/semantics/methods.k:106:6c0dfc288cc6

- Kind: `syntax`
- Lines: 106-106
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### reference-semantics/semantics/methods.k:107:31431694b27d

- Kind: `rule`
- Lines: 107-107
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### reference-semantics/semantics/methods.k:108:439491c83162

- Kind: `rule`
- Lines: 108-108
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### reference-semantics/semantics/methods.k:109:bd8e5ce805e4

- Kind: `rule`
- Lines: 109-111
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### reference-semantics/semantics/methods.k:112:d60af3772ac0

- Kind: `syntax`
- Lines: 112-112
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:113:885fc4123b60

- Kind: `rule`
- Lines: 113-113
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### reference-semantics/semantics/methods.k:115:9dc54db4cfe6

- Kind: `syntax`
- Lines: 115-115
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:116:35a981d9ee7c

- Kind: `rule`
- Lines: 116-116
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### reference-semantics/semantics/methods.k:118:219ceeed6ce7

- Kind: `syntax`
- Lines: 118-118
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:119:63bc2def4f48

- Kind: `rule`
- Lines: 119-119
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### reference-semantics/semantics/methods.k:121:86d0c30136f3

- Kind: `syntax`
- Lines: 121-121
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:122:12088c599f6a

- Kind: `rule`
- Lines: 122-122
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### reference-semantics/semantics/methods.k:124:79b65077c768

- Kind: `syntax`
- Lines: 124-124
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:125:f3875f726b38

- Kind: `rule`
- Lines: 125-125
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule hasUpper(.IntSeq) => false
```

### reference-semantics/semantics/methods.k:126:bb1d921fad33

- Kind: `rule`
- Lines: 126-126
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### reference-semantics/semantics/methods.k:128:6e2fe9388187

- Kind: `syntax`
- Lines: 128-128
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:129:abfddcd09b06

- Kind: `rule`
- Lines: 129-129
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule hasLower(.IntSeq) => false
```

### reference-semantics/semantics/methods.k:130:92b0385b9092

- Kind: `rule`
- Lines: 130-130
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### reference-semantics/semantics/methods.k:132:436a79dc0dbd

- Kind: `syntax`
- Lines: 132-132
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:133:2c1e5b1f9b4f

- Kind: `rule`
- Lines: 133-133
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule allAlpha(.IntSeq) => true
```

### reference-semantics/semantics/methods.k:134:5e18a35dd26e

- Kind: `rule`
- Lines: 134-134
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### reference-semantics/semantics/methods.k:136:1f98366143eb

- Kind: `syntax`
- Lines: 136-136
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:137:f2d51c623b4f

- Kind: `rule`
- Lines: 137-137
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule allDigit(.IntSeq) => true
```

### reference-semantics/semantics/methods.k:138:5aeec07d2a56

- Kind: `rule`
- Lines: 138-138
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### reference-semantics/semantics/methods.k:140:6bbb30e0ba93

- Kind: `syntax`
- Lines: 140-140
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:142:16ec3ccc73d9

- Kind: `rule`
- Lines: 142-142
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### reference-semantics/semantics/methods.k:143:90acf91ce794

- Kind: `rule`
- Lines: 143-143
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule lowerC(C:Int) => C         [owise]
```

### reference-semantics/semantics/methods.k:145:b6e1b4db46d4

- Kind: `syntax`
- Lines: 145-145
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= upperC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:146:36f1da2397a7

- Kind: `rule`
- Lines: 146-146
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### reference-semantics/semantics/methods.k:147:786ab98c703f

- Kind: `rule`
- Lines: 147-147
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule upperC(C:Int) => C         [owise]
```

### reference-semantics/semantics/methods.k:149:3d8ce436184a

- Kind: `syntax`
- Lines: 149-149
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= swapC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:150:ec05513118cd

- Kind: `rule`
- Lines: 150-150
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### reference-semantics/semantics/methods.k:151:960de195b818

- Kind: `rule`
- Lines: 151-151
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### reference-semantics/semantics/methods.k:152:88a95ca55d3e

- Kind: `rule`
- Lines: 152-152
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule swapC(C:Int) => C         [owise]
```

### reference-semantics/semantics/methods.k:154:0fb973df4891

- Kind: `syntax`
- Lines: 154-154
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:155:5cd9c020c2bd

- Kind: `rule`
- Lines: 155-155
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:156:da21f8430ee4

- Kind: `rule`
- Lines: 156-156
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### reference-semantics/semantics/methods.k:158:82523acd09b2

- Kind: `syntax`
- Lines: 158-158
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:159:b31cc456b204

- Kind: `rule`
- Lines: 159-159
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:160:2c01ef3cfffe

- Kind: `rule`
- Lines: 160-160
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### reference-semantics/semantics/methods.k:162:39e9100dbb4b

- Kind: `syntax`
- Lines: 162-162
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:163:6de81779e3a0

- Kind: `rule`
- Lines: 163-163
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:164:039a7b17bd02

- Kind: `rule`
- Lines: 164-164
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### reference-semantics/semantics/methods.k:166:6f6a4aa0687d

- Kind: `syntax`
- Lines: 166-166
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:167:7e2343bdac73

- Kind: `rule`
- Lines: 167-167
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### reference-semantics/semantics/methods.k:168:c22b5ffce270

- Kind: `rule`
- Lines: 168-168
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### reference-semantics/semantics/methods.k:169:4e5497c6f435

- Kind: `rule`
- Lines: 169-169
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### reference-semantics/semantics/methods.k:170:4c5df27adc71

- Kind: `endmodule`
- Lines: 170-170
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/operators.k:6:45e2448ad0cc

- Kind: `module`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-OPERATORS
```

### reference-semantics/semantics/operators.k:7:4258a966960e

- Kind: `imports`
- Lines: 7-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/operators.k:8:8ad41781e06e

- Kind: `imports`
- Lines: 8-8
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports MPY-ITER
```

### reference-semantics/semantics/operators.k:10:ec04b29e2d1b

- Kind: `rule`
- Lines: 10-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### reference-semantics/semantics/operators.k:12:c21855ae2fbb

- Kind: `rule`
- Lines: 12-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### reference-semantics/semantics/operators.k:15:e4932b24484a

- Kind: `context`
- Lines: 15-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  context Compare(HOLE, _)
```

### reference-semantics/semantics/operators.k:16:ca9e40a2c27b

- Kind: `context`
- Lines: 16-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### reference-semantics/semantics/operators.k:17:262226c0a44f

- Kind: `rule`
- Lines: 17-17
- Attributes: `owise`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### reference-semantics/semantics/operators.k:19:8ccf167a4ebc

- Kind: `rule`
- Lines: 19-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### reference-semantics/semantics/operators.k:20:0d4c09c2599c

- Kind: `rule`
- Lines: 20-24
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### reference-semantics/semantics/operators.k:25:5a6092f742c5

- Kind: `rule`
- Lines: 25-27
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/operators.k:28:75d0a7af5c82

- Kind: `rule`
- Lines: 28-33
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

### reference-semantics/semantics/operators.k:34:d56481fd1327

- Kind: `rule`
- Lines: 34-37
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### reference-semantics/semantics/operators.k:38:575d5da0be9c

- Kind: `rule`
- Lines: 38-42
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### reference-semantics/semantics/operators.k:44:0d606e97b2da

- Kind: `rule`
- Lines: 44-46
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/operators.k:47:4c5df27adc71

- Kind: `endmodule`
- Lines: 47-47
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/range.k:5:3245f59acaa6

- Kind: `module`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-RANGE
```

### reference-semantics/semantics/range.k:6:4258a966960e

- Kind: `imports`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/range.k:7:8ad41781e06e

- Kind: `imports`
- Lines: 7-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-ITER
```

### reference-semantics/semantics/range.k:9:dec39b9740c8

- Kind: `syntax`
- Lines: 9-9
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### reference-semantics/semantics/range.k:10:f93b1245c723

- Kind: `rule`
- Lines: 10-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### reference-semantics/semantics/range.k:12:9f9f1aaeaee2

- Kind: `syntax`
- Lines: 12-12
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### reference-semantics/semantics/range.k:13:9af49b302485

- Kind: `rule`
- Lines: 13-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### reference-semantics/semantics/range.k:15:d5350a65a2ba

- Kind: `rule`
- Lines: 15-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### reference-semantics/semantics/range.k:17:80ff51ad0241

- Kind: `rule`
- Lines: 17-18
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### reference-semantics/semantics/range.k:20:55e600477e36

- Kind: `rule`
- Lines: 20-22
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### reference-semantics/semantics/range.k:23:c4b766816492

- Kind: `rule`
- Lines: 23-24
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### reference-semantics/semantics/range.k:25:4c5df27adc71

- Kind: `endmodule`
- Lines: 25-25
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/set.k:3:a61579bc570f

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-SET
```

### reference-semantics/semantics/set.k:4:5dfb625da36c

- Kind: `imports`
- Lines: 4-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE

  // a set value, carried as its distinct codes in first-seen order (order is irrelevant
  // to membership/cardinality — the two observations sets support here).
```

### reference-semantics/semantics/set.k:8:288e97fc1a4c

- Kind: `syntax`
- Lines: 8-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### reference-semantics/semantics/set.k:11:be0ae2291d5d

- Kind: `syntax`
- Lines: 11-11
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### reference-semantics/semantics/set.k:12:f60a50831160

- Kind: `rule`
- Lines: 12-12
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### reference-semantics/semantics/set.k:13:908740ede17c

- Kind: `rule`
- Lines: 13-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### reference-semantics/semantics/set.k:16:dae5291dcfaa

- Kind: `syntax`
- Lines: 16-17
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### reference-semantics/semantics/set.k:18:d766b83ec2d8

- Kind: `rule`
- Lines: 18-18
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### reference-semantics/semantics/set.k:19:43f63938c987

- Kind: `rule`
- Lines: 19-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### reference-semantics/semantics/set.k:20:045bd0dd1ac5

- Kind: `rule`
- Lines: 20-21
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### reference-semantics/semantics/set.k:22:af80178bc6f5

- Kind: `rule`
- Lines: 22-23
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### reference-semantics/semantics/set.k:25:c59b599a912d

- Kind: `syntax`
- Lines: 25-25
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/set.k:26:c906946c4c7d

- Kind: `rule`
- Lines: 26-26
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### reference-semantics/semantics/set.k:27:a4561635907c

- Kind: `rule`
- Lines: 27-30
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### reference-semantics/semantics/set.k:31:b1d04ee84fab

- Kind: `syntax`
- Lines: 31-31
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/set.k:32:fb4a56d463fb

- Kind: `rule`
- Lines: 32-32
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### reference-semantics/semantics/set.k:33:850be538170a

- Kind: `rule`
- Lines: 33-33
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### reference-semantics/semantics/set.k:35:6156266fe9d9

- Kind: `syntax`
- Lines: 35-35
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/set.k:36:aa7872fffe94

- Kind: `rule`
- Lines: 36-38
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### reference-semantics/semantics/set.k:39:7a5ed6b4e8d6

- Kind: `rule`
- Lines: 39-39
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### reference-semantics/semantics/set.k:40:4c5df27adc71

- Kind: `endmodule`
- Lines: 40-40
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/sort.k:10:2324159bdf28

- Kind: `module`
- Lines: 10-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-SORT
```

### reference-semantics/semantics/sort.k:11:513b07985ad1

- Kind: `imports`
- Lines: 11-11
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-BUILTINS
```

### reference-semantics/semantics/sort.k:12:3b7d30bdfb44

- Kind: `imports`
- Lines: 12-17
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-SUBSCRIPT

  // sortVS(VS): the ascending sort of the Val list VS. Opaque for symbolic VS (no-evaluators);
  // concrete insertion sort for krun.
  // Concrete sort matches Int-sorted elements directly (an int Val IS an Int); projectIntTotal
  // (lemmas-only) is not available in the semantics. Int and str lists.
```

### reference-semantics/semantics/sort.k:18:c6d761b986e3

- Kind: `syntax`
- Lines: 18-18
- Attributes: `function`, `symbol(sortVS)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### reference-semantics/semantics/sort.k:19:0a76cca66b26

- Kind: `syntax`
- Lines: 19-19
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### reference-semantics/semantics/sort.k:20:6bd401e364fe

- Kind: `rule`
- Lines: 20-20
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### reference-semantics/semantics/sort.k:21:afe20c3cfa1a

- Kind: `rule`
- Lines: 21-21
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### reference-semantics/semantics/sort.k:22:0e61d8cbcf24

- Kind: `rule`
- Lines: 22-22
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### reference-semantics/semantics/sort.k:23:e38dbfdea30a

- Kind: `rule`
- Lines: 23-23
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### reference-semantics/semantics/sort.k:24:ecd0fc7b5c1f

- Kind: `rule`
- Lines: 24-25
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### reference-semantics/semantics/sort.k:26:f778a322aece

- Kind: `syntax`
- Lines: 26-26
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### reference-semantics/semantics/sort.k:27:f56269f2805f

- Kind: `rule`
- Lines: 27-27
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### reference-semantics/semantics/sort.k:28:1f2df95775eb

- Kind: `rule`
- Lines: 28-28
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### reference-semantics/semantics/sort.k:29:302f44585998

- Kind: `rule`
- Lines: 29-30
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### reference-semantics/semantics/sort.k:31:417317762dc3

- Kind: `rule`
- Lines: 31-35
- Attributes: `concrete`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

### reference-semantics/semantics/sort.k:36:b80d34d1b4d6

- Kind: `rule`
- Lines: 36-39
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### reference-semantics/semantics/sort.k:40:2f7f7ea23353

- Kind: `rule`
- Lines: 40-48
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]

  // ==== keyed / reversed sorted() (WP2) =====================================
  // sortKeyVS(VS, KV): the stable ascending sort of VS by the key value KV
  // (a closure/builtin/type — anything callable). OPAQUE here; the concrete
  // leg (MPY-CONCRETE, llvm only) computes keys by REAL calls and stable-
  // inserts, at priority(40) over these.
```

### reference-semantics/semantics/sort.k:49:f2ac55ee34d8

- Kind: `syntax`
- Lines: 49-49
- Attributes: `function`, `symbol(sortKeyVS)`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### reference-semantics/semantics/sort.k:51:da8fbe9dd99b

- Kind: `syntax`
- Lines: 51-52
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### reference-semantics/semantics/sort.k:53:ce0aa18a5360

- Kind: `rule`
- Lines: 53-53
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### reference-semantics/semantics/sort.k:54:726a2866a59e

- Kind: `rule`
- Lines: 54-54
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### reference-semantics/semantics/sort.k:55:5fd679052347

- Kind: `rule`
- Lines: 55-55
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### reference-semantics/semantics/sort.k:57:7e8ff8d017c7

- Kind: `syntax`
- Lines: 57-57
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### reference-semantics/semantics/sort.k:58:a1e37b0851c3

- Kind: `rule`
- Lines: 58-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule condRev(S:ValSeq, false) => S
```

### reference-semantics/semantics/sort.k:59:b59c3f4a824c

- Kind: `rule`
- Lines: 59-59
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### reference-semantics/semantics/sort.k:61:72cacce57534

- Kind: `rule`
- Lines: 61-62
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### reference-semantics/semantics/sort.k:63:9934b02daf55

- Kind: `rule`
- Lines: 63-64
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### reference-semantics/semantics/sort.k:65:1ce051984ec6

- Kind: `rule`
- Lines: 65-71
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
```

### reference-semantics/semantics/sort.k:72:4c5df27adc71

- Kind: `endmodule`
- Lines: 72-72
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/str.k:3:6e503b11331c

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-STR
```

### reference-semantics/semantics/str.k:4:4258a966960e

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/str.k:5:4c55a93b575a

- Kind: `imports`
- Lines: 5-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-ITER

  // ==== iteration (the iterator protocol's str case; yields 1-char strings) ==
```

### reference-semantics/semantics/str.k:8:c96529154572

- Kind: `rule`
- Lines: 8-8
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### reference-semantics/semantics/str.k:9:d785d2163878

- Kind: `rule`
- Lines: 9-12
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### reference-semantics/semantics/str.k:13:4c7f66efcd88

- Kind: `syntax`
- Lines: 13-13
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### reference-semantics/semantics/str.k:14:70d0a8a99357

- Kind: `rule`
- Lines: 14-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### reference-semantics/semantics/str.k:15:c7b4b4fc80bd

- Kind: `rule`
- Lines: 15-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strToCodes("") => .IntSeq
```

### reference-semantics/semantics/str.k:16:277e19f524bc

- Kind: `rule`
- Lines: 16-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

### reference-semantics/semantics/str.k:20:4dcfe32d71db

- Kind: `syntax`
- Lines: 20-20
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:21:1bc8690035f0

- Kind: `rule`
- Lines: 21-21
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### reference-semantics/semantics/str.k:22:b8aaa07a8414

- Kind: `rule`
- Lines: 22-22
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### reference-semantics/semantics/str.k:24:6b69c6c1fd75

- Kind: `rule`
- Lines: 24-24
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### reference-semantics/semantics/str.k:25:8039b62069c1

- Kind: `rule`
- Lines: 25-25
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### reference-semantics/semantics/str.k:26:38a24a190cf2

- Kind: `rule`
- Lines: 26-28
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### reference-semantics/semantics/str.k:29:44d8a30fde58

- Kind: `rule`
- Lines: 29-29
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### reference-semantics/semantics/str.k:30:b646f3d3387b

- Kind: `rule`
- Lines: 30-30
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### reference-semantics/semantics/str.k:32:0c2a240d2f88

- Kind: `syntax`
- Lines: 32-32
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:33:57c619a4cc23

- Kind: `rule`
- Lines: 33-33
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### reference-semantics/semantics/str.k:34:0e758c7b129d

- Kind: `rule`
- Lines: 34-34
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### reference-semantics/semantics/str.k:35:d6816398ab16

- Kind: `rule`
- Lines: 35-35
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### reference-semantics/semantics/str.k:37:e5d82a70ec2a

- Kind: `syntax`
- Lines: 37-37
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:38:fe5302406eba

- Kind: `rule`
- Lines: 38-38
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### reference-semantics/semantics/str.k:39:6c197a2767cc

- Kind: `rule`
- Lines: 39-39
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### reference-semantics/semantics/str.k:40:04c4c5381ecb

- Kind: `rule`
- Lines: 40-47
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))

  // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
  // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
  // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
  // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
  // str </<=/>/>= comparisons.
```

### reference-semantics/semantics/str.k:48:e6a79420c495

- Kind: `syntax`
- Lines: 48-48
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:49:d9faa5615105

- Kind: `rule`
- Lines: 49-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### reference-semantics/semantics/str.k:50:1d055a6c97d4

- Kind: `rule`
- Lines: 50-50
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### reference-semantics/semantics/str.k:51:d1e1c922c4b2

- Kind: `rule`
- Lines: 51-51
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### reference-semantics/semantics/str.k:52:a15116dcda03

- Kind: `rule`
- Lines: 52-52
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### reference-semantics/semantics/str.k:53:7c98b79b0e03

- Kind: `rule`
- Lines: 53-53
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### reference-semantics/semantics/str.k:54:d72e4a9c68cd

- Kind: `rule`
- Lines: 54-54
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### reference-semantics/semantics/str.k:56:3f16844c8a96

- Kind: `rule`
- Lines: 56-56
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### reference-semantics/semantics/str.k:57:d14e65d751c2

- Kind: `rule`
- Lines: 57-57
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### reference-semantics/semantics/str.k:58:fd8254e2aad6

- Kind: `rule`
- Lines: 58-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### reference-semantics/semantics/str.k:59:0bb37c9e5117

- Kind: `rule`
- Lines: 59-59
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### reference-semantics/semantics/str.k:60:4c5df27adc71

- Kind: `endmodule`
- Lines: 60-60
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/subscript.k:3:a6d1f94e4e77

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-SUBSCRIPT
```

### reference-semantics/semantics/subscript.k:4:547ab1e4cdcd

- Kind: `imports`
- Lines: 4-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE

  // ==== positional access + negative-index normalization (used only here) ===
  // valSeqAt is [total]: in-bounds vCons access reduces as usual; on an OPAQUE sequence (e.g.
  // a trusted sort's sortVS(VS)) or OOB it stays an abstract total value — so indexing the
  // opaque sorted list is DEFINED (no undischarged #Ceil), matching the old semantics' total
  // atK. K trusts the [total] annotation; valid programs index in-bounds.
```

### reference-semantics/semantics/subscript.k:11:92dd5a3cbdae

- Kind: `syntax`
- Lines: 11-11
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:12:5efae5e63665

- Kind: `rule`
- Lines: 12-12
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### reference-semantics/semantics/subscript.k:13:463bd5d63df5

- Kind: `rule`
- Lines: 13-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### reference-semantics/semantics/subscript.k:16:d573fee41395

- Kind: `syntax`
- Lines: 16-16
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### reference-semantics/semantics/subscript.k:17:8eb9da7cc045

- Kind: `rule`
- Lines: 17-17
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### reference-semantics/semantics/subscript.k:18:a89deb267298

- Kind: `rule`
- Lines: 18-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### reference-semantics/semantics/subscript.k:21:8d0629ddf60a

- Kind: `syntax`
- Lines: 21-21
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:22:0398dfbaabb1

- Kind: `rule`
- Lines: 22-22
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### reference-semantics/semantics/subscript.k:23:be71b64b7c4b

- Kind: `rule`
- Lines: 23-26
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### reference-semantics/semantics/subscript.k:27:e235a553cf79

- Kind: `context`
- Lines: 27-27
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  context Subscript(HOLE, _)
```

### reference-semantics/semantics/subscript.k:28:5ee62afca97f

- Kind: `context`
- Lines: 28-30
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### reference-semantics/semantics/subscript.k:31:ba2015156656

- Kind: `rule`
- Lines: 31-33
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/subscript.k:35:e2cbe99533f0

- Kind: `rule`
- Lines: 35-35
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### reference-semantics/semantics/subscript.k:37:83aa86951e42

- Kind: `syntax`
- Lines: 37-37
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### reference-semantics/semantics/subscript.k:38:c494188c31ef

- Kind: `rule`
- Lines: 38-38
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### reference-semantics/semantics/subscript.k:39:52ab84557b24

- Kind: `rule`
- Lines: 39-39
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### reference-semantics/semantics/subscript.k:40:02afdec95b66

- Kind: `rule`
- Lines: 40-43
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### reference-semantics/semantics/subscript.k:44:3586c0bf2e67

- Kind: `syntax`
- Lines: 44-47
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### reference-semantics/semantics/subscript.k:49:560ebb71a2e1

- Kind: `syntax`
- Lines: 49-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### reference-semantics/semantics/subscript.k:50:260093ac1ada

- Kind: `rule`
- Lines: 50-50
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### reference-semantics/semantics/subscript.k:51:c05e824ec7d0

- Kind: `rule`
- Lines: 51-51
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### reference-semantics/semantics/subscript.k:52:55c49487ba78

- Kind: `rule`
- Lines: 52-52
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### reference-semantics/semantics/subscript.k:54:b39cd50c6c41

- Kind: `rule`
- Lines: 54-54
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### reference-semantics/semantics/subscript.k:55:ba8162a4d944

- Kind: `rule`
- Lines: 55-55
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### reference-semantics/semantics/subscript.k:56:0a67a100f00e

- Kind: `rule`
- Lines: 56-57
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### reference-semantics/semantics/subscript.k:58:8d45174aef87

- Kind: `rule`
- Lines: 58-60
- Attributes: `priority(45)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### reference-semantics/semantics/subscript.k:61:4b6c937f1b27

- Kind: `rule`
- Lines: 61-61
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### reference-semantics/semantics/subscript.k:63:35803b4f4140

- Kind: `syntax`
- Lines: 63-63
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### reference-semantics/semantics/subscript.k:64:f98c4d73aaf2

- Kind: `rule`
- Lines: 64-65
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### reference-semantics/semantics/subscript.k:66:6e8f59ed2ecb

- Kind: `rule`
- Lines: 66-67
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### reference-semantics/semantics/subscript.k:68:0b28898fb685

- Kind: `rule`
- Lines: 68-71
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### reference-semantics/semantics/subscript.k:72:3673727509ac

- Kind: `syntax`
- Lines: 72-72
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### reference-semantics/semantics/subscript.k:73:080183421a02

- Kind: `rule`
- Lines: 73-73
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slStep(noB)          => 1
```

### reference-semantics/semantics/subscript.k:74:38520b2d08df

- Kind: `rule`
- Lines: 74-74
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slStep(someB(S:Int)) => S
```

### reference-semantics/semantics/subscript.k:76:12940b25c9d8

- Kind: `syntax`
- Lines: 76-76
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### reference-semantics/semantics/subscript.k:77:f071f630a8f9

- Kind: `rule`
- Lines: 77-78
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### reference-semantics/semantics/subscript.k:79:9a3afd20003e

- Kind: `rule`
- Lines: 79-80
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### reference-semantics/semantics/subscript.k:81:2e19a63f1664

- Kind: `rule`
- Lines: 81-81
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### reference-semantics/semantics/subscript.k:83:def902114717

- Kind: `syntax`
- Lines: 83-83
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### reference-semantics/semantics/subscript.k:84:f8868ca0ab86

- Kind: `rule`
- Lines: 84-85
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### reference-semantics/semantics/subscript.k:86:fde349e77a3a

- Kind: `rule`
- Lines: 86-87
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### reference-semantics/semantics/subscript.k:88:8422a8ba8f8d

- Kind: `rule`
- Lines: 88-88
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### reference-semantics/semantics/subscript.k:90:9ec1896aa81d

- Kind: `syntax`
- Lines: 90-90
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:91:58c9216d8b6d

- Kind: `rule`
- Lines: 91-92
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### reference-semantics/semantics/subscript.k:93:1c4d6ca3d353

- Kind: `rule`
- Lines: 93-94
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### reference-semantics/semantics/subscript.k:96:74b1e671d5bc

- Kind: `syntax`
- Lines: 96-96
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:97:a2e92eace44c

- Kind: `rule`
- Lines: 97-98
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### reference-semantics/semantics/subscript.k:99:0a357da8ed32

- Kind: `rule`
- Lines: 99-100
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### reference-semantics/semantics/subscript.k:102:cf49fd584aa0

- Kind: `syntax`
- Lines: 102-102
- Attributes: `function`, `total`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:103:706a4096d6ec

- Kind: `rule`
- Lines: 103-104
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### reference-semantics/semantics/subscript.k:105:b3f79aaddc21

- Kind: `rule`
- Lines: 105-108
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

### reference-semantics/semantics/subscript.k:109:328023ed0539

- Kind: `syntax`
- Lines: 109-109
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### reference-semantics/semantics/subscript.k:110:d6ecccf0b62d

- Kind: `rule`
- Lines: 110-112
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### reference-semantics/semantics/subscript.k:113:0150c19c3715

- Kind: `rule`
- Lines: 113-114
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### reference-semantics/semantics/subscript.k:116:0a55bc39332c

- Kind: `syntax`
- Lines: 116-116
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### reference-semantics/semantics/subscript.k:117:723e67f7af3e

- Kind: `rule`
- Lines: 117-119
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### reference-semantics/semantics/subscript.k:120:68b366dedd7d

- Kind: `rule`
- Lines: 120-121
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### reference-semantics/semantics/subscript.k:122:4c5df27adc71

- Kind: `endmodule`
- Lines: 122-122
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### reference-semantics/semantics/syntax.k:3:f08baa14168e

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
module MPY-SYNTAX
```

### reference-semantics/semantics/syntax.k:4:549ff9577e48

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports INT-SYNTAX
```

### reference-semantics/semantics/syntax.k:5:57afda1786d2

- Kind: `imports`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports FLOAT-SYNTAX
```

### reference-semantics/semantics/syntax.k:6:53df7c7bde97

- Kind: `imports`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports BOOL-SYNTAX
```

### reference-semantics/semantics/syntax.k:7:5a171c0d093c

- Kind: `imports`
- Lines: 7-7
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  imports STRING-SYNTAX
```

### reference-semantics/semantics/syntax.k:9:970a5d907eb7

- Kind: `syntax`
- Lines: 9-30
- Attributes: `macro`, `strict(1)`, `strict(2)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Expr ::= "Int"      "(" Int ")"
                | "Float"    "(" Float ")"
                | "Bool"     "(" Bool ")"
                | "Name"     "(" String ")"
                | "Str"      "(" String ")"
                | "UnaryOp"  "(" String "," Expr ")" [strict(2)]
                | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)]
                | "BoolOp"    "(" String "," Exprs ")"
                | "ListExpr"  "(" Exprs ")"
                | "DictExpr"  "(" Entries ")"
                | "ListComp"  "(" Expr "," CompFors ")" [macro]
                | "GenExp"    "(" Expr "," CompFors ")" [macro]
                | "TupleExpr" "(" Exprs ")"
                | "Subscript" "(" Expr "," Index ")"
                | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)]
                | "Lambda"    "(" Params "," Expr ")"
                | "KwArg"     "(" String "," Expr ")"
                | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")"
                | "NoneVal"
                | "Call"      "(" Expr "," Exprs ")"
                | "Attribute" "(" Expr "," String ")" [strict(1)]
                | "Compare"   "(" Expr "," CmpOp ")"
```

### reference-semantics/semantics/syntax.k:32:31fa5777bd64

- Kind: `syntax`
- Lines: 32-32
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### reference-semantics/semantics/syntax.k:33:3bf94dbad23a

- Kind: `syntax`
- Lines: 33-33
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### reference-semantics/semantics/syntax.k:34:0e6de400c483

- Kind: `syntax`
- Lines: 34-34
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Entries  ::= List{Entry, ","}
```

### reference-semantics/semantics/syntax.k:35:5bb59c5f0dc1

- Kind: `syntax`
- Lines: 35-35
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### reference-semantics/semantics/syntax.k:36:76d2ff7278fb

- Kind: `syntax`
- Lines: 36-36
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax CompFors ::= List{CompFor, ""}
```

### reference-semantics/semantics/syntax.k:37:5d0831f6c932

- Kind: `syntax`
- Lines: 37-37
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Exprs    ::= List{Expr, ","}
```

### reference-semantics/semantics/syntax.k:38:2d7648621bd0

- Kind: `syntax`
- Lines: 38-38
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### reference-semantics/semantics/syntax.k:39:0a207e7f6805

- Kind: `syntax`
- Lines: 39-39
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Bound    ::= Expr | "NoBound"
```

### reference-semantics/semantics/syntax.k:41:1fdf12132fa6

- Kind: `syntax`
- Lines: 41-54
- Attributes: `strict`, `strict(1)`, `strict(2)`, `strict(3)`
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)]
                | "Import"    "(" String ")"
                | "ImportFrom" "(" String "," ParamNames ")"
                | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)]
                | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)]
                | "While"     "(" Expr "," Stmts ")"
                | "Break"
                | "Continue"
                | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)]
                | "Return"    "(" Expr ")" [strict]
                | "Assert"    "(" Expr ")" [strict]
                | "Expr"      "(" Expr ")" [strict]
                | "FuncDef"   "(" String "," Params "," Stmts ")"
                | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
```

### reference-semantics/semantics/syntax.k:56:a815785974c2

- Kind: `syntax`
- Lines: 56-56
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### reference-semantics/semantics/syntax.k:57:f9fd64833dd1

- Kind: `syntax`
- Lines: 57-57
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### reference-semantics/semantics/syntax.k:58:19c7da008dd6

- Kind: `syntax`
- Lines: 58-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### reference-semantics/semantics/syntax.k:59:ff2cf5e4bb87

- Kind: `syntax`
- Lines: 59-59
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### reference-semantics/semantics/syntax.k:60:8788a8da7c08

- Kind: `syntax`
- Lines: 60-60
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax ParamNames ::= List{String, ","}
```

### reference-semantics/semantics/syntax.k:61:8da28960d4db

- Kind: `syntax`
- Lines: 61-61
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### reference-semantics/semantics/syntax.k:62:4c5df27adc71

- Kind: `endmodule`
- Lines: 62-62
- Attributes: none
- Decision: `FIXED_SUPPLIED_MATERIAL_MODULE`
- Rationale: Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.

```k
endmodule
```

### reference-semantics/semantics/tuple.k:3:a660cd1e92e2

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
module MPY-TUPLE
```

### reference-semantics/semantics/tuple.k:4:4258a966960e

- Kind: `imports`
- Lines: 4-4
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-CORE
```

### reference-semantics/semantics/tuple.k:5:8ad41781e06e

- Kind: `imports`
- Lines: 5-5
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-ITER
```

### reference-semantics/semantics/tuple.k:6:511c798e04e9

- Kind: `imports`
- Lines: 6-6
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-LIST
```

### reference-semantics/semantics/tuple.k:7:1e2cd5461704

- Kind: `imports`
- Lines: 7-9
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  imports MPY-METHODS

  // ==== iteration (the iterator protocol's tuple case) ======================
```

### reference-semantics/semantics/tuple.k:10:6088fae06255

- Kind: `rule`
- Lines: 10-10
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### reference-semantics/semantics/tuple.k:11:354a4a5539b7

- Kind: `rule`
- Lines: 11-13
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### reference-semantics/semantics/tuple.k:14:508a95f61aed

- Kind: `syntax`
- Lines: 14-14
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax ApplyK ::= "toTuple"
```

### reference-semantics/semantics/tuple.k:15:ff193ea2849e

- Kind: `rule`
- Lines: 15-15
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### reference-semantics/semantics/tuple.k:16:b0d84d481730

- Kind: `rule`
- Lines: 16-16
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### reference-semantics/semantics/tuple.k:18:bf0ac96e9f03

- Kind: `rule`
- Lines: 18-19
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### reference-semantics/semantics/tuple.k:20:4e02486b9482

- Kind: `rule`
- Lines: 20-20
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### reference-semantics/semantics/tuple.k:21:feaa26e61df6

- Kind: `rule`
- Lines: 21-22
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### reference-semantics/semantics/tuple.k:23:bd7254bbf110

- Kind: `rule`
- Lines: 23-23
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### reference-semantics/semantics/tuple.k:24:df13ef70912b

- Kind: `syntax`
- Lines: 24-24
- Attributes: `function`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### reference-semantics/semantics/tuple.k:25:663f7ddf889d

- Kind: `rule`
- Lines: 25-25
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### reference-semantics/semantics/tuple.k:26:11dc3e7b5407

- Kind: `rule`
- Lines: 26-27
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### reference-semantics/semantics/tuple.k:28:796dabf5001e

- Kind: `rule`
- Lines: 28-30
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### reference-semantics/semantics/tuple.k:31:98b229b9b432

- Kind: `syntax`
- Lines: 31-31
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### reference-semantics/semantics/tuple.k:32:c3fab775730b

- Kind: `rule`
- Lines: 32-34
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### reference-semantics/semantics/tuple.k:35:bc76f6241e7d

- Kind: `rule`
- Lines: 35-41
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### reference-semantics/semantics/tuple.k:42:0d5b4092fa17

- Kind: `rule`
- Lines: 42-42
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:43:a816acd68173

- Kind: `rule`
- Lines: 43-43
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:44:a50c06a62842

- Kind: `rule`
- Lines: 44-48
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### reference-semantics/semantics/tuple.k:49:7dbe45ad3aa2

- Kind: `syntax`
- Lines: 49-49
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### reference-semantics/semantics/tuple.k:50:3187abeadb72

- Kind: `rule`
- Lines: 50-50
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:51:441a29fab67a

- Kind: `rule`
- Lines: 51-51
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:52:f7778b444162

- Kind: `rule`
- Lines: 52-54
- Attributes: `priority(40)`
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/tuple.k:55:d538f44e4a19

- Kind: `rule`
- Lines: 55-56
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:57:2377fb943da1

- Kind: `rule`
- Lines: 57-57
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### reference-semantics/semantics/tuple.k:58:4c5df27adc71

- Kind: `endmodule`
- Lines: 58-58
- Attributes: none
- Decision: `FIXED_SUPPLIED_UNUSED_MODULE`
- Rationale: Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.

```k
endmodule
```

### verification.k:1:1c2b9a0599db

- Kind: `requires`
- Lines: 1-1
- Attributes: none
- Decision: `STRUCTURE`
- Rationale: Module/import structure.

```k
requires "reference-semantics/semantics.k"
```

### verification.k:3:9dda73b03276

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `STRUCTURE`
- Rationale: Module/import structure.

```k
module VERIFICATION
```

### verification.k:4:e4cf057623c0

- Kind: `imports`
- Lines: 4-6
- Attributes: none
- Decision: `STRUCTURE`
- Rationale: Module/import structure.

```k
  imports MPY

  // Explicit form of Map deletion used by function-frame teardown.
```

### verification.k:7:75f08df4443d

- Kind: `rule`
- Lines: 7-9
- Attributes: `simplification`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule (((X:KItem |-> _:KItem) M:Map) [ X <- undef ]) => M
       requires notBool (X in_keys(M))
       [simplification]
```

### verification.k:10:517173a5f678

- Kind: `rule`
- Lines: 10-17
- Attributes: `simplification`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule (M:Map [ X:KItem <- V:KItem ]) => (X |-> V) M
       requires notBool (X in_keys(M))
       [simplification]

  // Proof-normalization lemmas for ordinary (non-closure-cell) frames.  These
  // are guarded specializations of MPY's existing rules; the priority prevents
  // the symbolic prover from exploring impossible cellRef branches after the
  // guard has established that "$cells" is absent.
```

### verification.k:18:be0b2d497bd1

- Kind: `rule`
- Lines: 18-22
- Attributes: `priority(39)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Name(X:String) => {M[X]}:>Val ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M) andBool notBool ("$cells" in_keys(M))
       [priority(39)]
```

### verification.k:24:5782f0eb2e7b

- Kind: `rule`
- Lines: 24-29
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Name(X:String) => V:Val ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> V) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]
```

### verification.k:31:8d689f894676

- Kind: `rule`
- Lines: 31-39
- Attributes: `priority(39)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _:Parent) ... </scopes>
       requires notBool ("$cells" in_keys(M))
       [priority(39)]

  // Direct literal cooling, equivalent to Int(I) => I followed by Assign's
  // strictness context.  Keeping it explicit avoids a symbolic freezer branch
  // at loop-summary boundaries.
```

### verification.k:40:76e475116b21

- Kind: `rule`
- Lines: 40-41
- Attributes: `priority(39)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Assign(Name(X:String), Int(I:Int)) => Assign(Name(X), I) ... </k>
       [priority(39)]
```

### verification.k:43:a57a6a94d538

- Kind: `rule`
- Lines: 43-44
- Attributes: `priority(39)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Assign(Name(X:String), Bool(B:Bool)) => Assign(Name(X), B) ... </k>
       [priority(39)]
```

### verification.k:46:88364b54609b

- Kind: `rule`
- Lines: 46-53
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         ((X |-> _:Val) M:Map => (X |-> V) M),
         _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]
```

### verification.k:55:096701064bf6

- Kind: `rule`
- Lines: 55-63
- Attributes: `priority(39)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ],
         _:Parent) ... </scopes>
       requires X in_keys(M)
         andBool notBool ("$cells" in_keys(M))
         andBool notBool isRefV({M[X]}:>Val)
       [priority(39)]
```

### verification.k:65:1f117a6bfc86

- Kind: `rule`
- Lines: 65-73
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         ((X |-> A:Val) M:Map => (X |-> applyBin(OP, A, V)) M),
         _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> A) M))
         andBool notBool isRefV(A)
       [priority(38)]
```

### verification.k:75:f882a551f6bd

- Kind: `rule`
- Lines: 75-79
- Attributes: `priority(39)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _:Parent) ... </scopes>
       requires notBool ("$cells" in_keys(M))
       [priority(39)]
```

### verification.k:81:83d93593919a

- Kind: `rule`
- Lines: 81-90
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         ((X |-> _:Val) M:Map => (X |-> V) M),
         _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]

  // Strictness-normalized forms used by the outer list loop.
```

### verification.k:91:317846085194

- Kind: `rule`
- Lines: 91-101
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Compare(Name(X:String), CmpOp(OP:String, Name(Y:String)))
        => applyCmp(OP, A, B) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         (X |-> A:Val) (Y |-> B:Val) M:Map,
         _:Parent) ... </scopes>
       requires X =/=String Y
         andBool notBool (X in_keys(M))
         andBool notBool (Y in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> A) (Y |-> B) M))
       [priority(38)]
```

### verification.k:103:8eac960c29df

- Kind: `rule`
- Lines: 103-109
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Compare(Name(X:String), CmpOp(OP:String, Int(I:Int)))
        => applyCmp(OP, A, I) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> A:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> A) M))
       [priority(38)]
```

### verification.k:111:093489693192

- Kind: `rule`
- Lines: 111-117
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> If(Name(X:String), T:Stmts, E:Stmts)
        => #branch(truthy(V), T, E) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> V:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]
```

### verification.k:119:715316220cab

- Kind: `rule`
- Lines: 119-125
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Assign(Name(X:String), Name(Y:String))
        => Assign(Name(X), V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((Y |-> V:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (Y in_keys(M))
         andBool notBool ("$cells" in_keys((Y |-> V) M))
       [priority(38)]
```

### verification.k:127:64c784a06962

- Kind: `rule`
- Lines: 127-132
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> Return(Name(X:String)) => Return(V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> V:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]
```

### verification.k:134:ee24f0b23184

- Kind: `rule`
- Lines: 134-140
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k> For(T:Expr, Name(X:String), B:Stmts)
        => #loop(V, T, B) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> V:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]
```

### verification.k:142:59d0bed57f68

- Kind: `rule`
- Lines: 142-164
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k>
         Call(
           Name("skjkasdkd"),
           (list(asVals(IS:IntList)), .Exprs))
        => #applyK(
             toCall(closureVal(
               ("lst", .ParamNames),
               #functionBody,
               0)),
             (list(asVals(IS)), .Vals)) ...
       </k>
       <env> 0 </env>
       <scopes>
         ... 0 |-> scope(
           ("skjkasdkd" |-> closureVal(
             ("lst", .ParamNames),
             #functionBody,
             0))
           M:Map,
           parent(-1)) ...
       </scopes>
       requires notBool ("skjkasdkd" in_keys(M))
       [priority(38)]
```

### verification.k:166:0e4e3ccd00e9

- Kind: `rule`
- Lines: 166-180
- Attributes: `priority(38)`
- Decision: `SOUND_FIXED_RULE_SPECIALIZATION`
- Rationale: Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.

```k
  rule <k>
         Assign(
           Name("prime"),
           Compare(Name("number"), CmpOp(">=", Int(2))))
        => Assign(Name("prime"), N >=Int 2) ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(("number" |-> N:Int) M:Map, _:Parent) ... </scopes>
       requires notBool ("number" in_keys(M))
         andBool notBool ("$cells" in_keys(("number" |-> N) M))
       [priority(38)]

  // Integer-only input lists.  This sort makes the task's stated input
  // precondition structural, so symbolic execution never admits a non-int
  // element.
```

### verification.k:181:d4299f9986b9

- Kind: `syntax`
- Lines: 181-181
- Attributes: none
- Decision: `SOUND_DOMAIN_SYNTAX`
- Rationale: Unbounded recursive IntList domain; represents every finite integer sequence.

```k
  syntax IntList ::= ".IntList" | intCons(Int, IntList)
```

### verification.k:183:6cf8298b3abe

- Kind: `syntax`
- Lines: 183-185
- Attributes: none
- Decision: `INPUT_REPRESENTATION_SYMBOL`
- Rationale: Proof-side sequence representation. Its only material consumer is covered by the two structural iterator rules.

```k
  syntax ValSeq ::= asVals(IntList)

  // Structural iterator cases expose IntList's constructors to narrowing.
```

### verification.k:186:e48ba4c9d7c3

- Kind: `rule`
- Lines: 186-187
- Attributes: `priority(39)`
- Decision: `SOUND_INPUT_REPRESENTATION_RULE`
- Rationale: Constructor-complete iterator behavior for empty/cons IntList; no result oracle is introduced.

```k
  rule <k> #iterNext(list(asVals(.IntList))) => #iterDone ... </k>
       [priority(39)]
```

### verification.k:188:2c8a17f3f5c8

- Kind: `rule`
- Lines: 188-193
- Attributes: `priority(39)`
- Decision: `SOUND_INPUT_REPRESENTATION_RULE`
- Rationale: Constructor-complete iterator behavior for empty/cons IntList; no result oracle is introduced.

```k
  rule <k> #iterNext(list(asVals(intCons(I:Int, IS:IntList))))
        => #iterYield(I, list(asVals(IS))) ... </k>
       [priority(39)]

  // The mathematical primality oracle follows the implementation's trial
  // division exactly.  false means that an earlier divisor was already found.
```

### verification.k:194:00b91c3a04c2

- Kind: `syntax`
- Lines: 194-194
- Attributes: `function`, `total`
- Decision: `LIMITED_TOTALITY_DECLARATION`
- Rationale: Truthful and complete on the claim-reachable D>=2 domain; [total] is not globally covered at D=0 because pyMod(N,0) is undefined.

```k
  syntax Bool ::= trialPrime(Int, Int, Bool) [function, total]
```

### verification.k:195:84d051c72ba6

- Kind: `rule`
- Lines: 195-195
- Attributes: none
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule trialPrime(_:Int, _:Int, false) => false
```

### verification.k:196:d69677cf22d7

- Kind: `rule`
- Lines: 196-197
- Attributes: none
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule trialPrime(N:Int, D:Int, true) => true
    requires D *Int D >Int N
```

### verification.k:198:3514b37ece5f

- Kind: `rule`
- Lines: 198-200
- Attributes: `simplification`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule trialPrime(N:Int, D:Int, true) => false
    requires D *Int D <=Int N andBool pyMod(N, D) ==Int 0
    [simplification]
```

### verification.k:201:38a4060325d1

- Kind: `rule`
- Lines: 201-207
- Attributes: `simplification`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule trialPrime(N:Int, D:Int, true) => trialPrime(N, D +Int 1, true)
    requires D *Int D <=Int N
      andBool notBool (pyMod(N, D) ==Int 0)
    [simplification]

  // The final divisor value is specified too, allowing the loop invariant to
  // describe the whole local store rather than hiding a side effect.
```

### verification.k:208:9540c80f2d68

- Kind: `syntax`
- Lines: 208-208
- Attributes: `function`, `total`
- Decision: `LIMITED_TOTALITY_DECLARATION`
- Rationale: Truthful and complete on the claim-reachable D>=2 domain; [total] is not globally covered at D=0 because pyMod(N,0) is undefined.

```k
  syntax Int ::= trialDivisor(Int, Int, Bool) [function, total]
```

### verification.k:209:73b6ee7287da

- Kind: `rule`
- Lines: 209-209
- Attributes: none
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule trialDivisor(_:Int, D:Int, false) => D
```

### verification.k:210:493abb948eae

- Kind: `rule`
- Lines: 210-211
- Attributes: none
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule trialDivisor(N:Int, D:Int, true) => D
    requires D *Int D >Int N
```

### verification.k:212:575689060dcf

- Kind: `rule`
- Lines: 212-214
- Attributes: `simplification`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule trialDivisor(N:Int, D:Int, true) => D +Int 1
    requires D *Int D <=Int N andBool pyMod(N, D) ==Int 0
    [simplification]
```

### verification.k:215:c5e9f2d036dd

- Kind: `rule`
- Lines: 215-219
- Attributes: `simplification`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule trialDivisor(N:Int, D:Int, true)
    => trialDivisor(N, D +Int 1, true)
    requires D *Int D <=Int N
      andBool notBool (pyMod(N, D) ==Int 0)
    [simplification]
```

### verification.k:221:b48dd2ecceb0

- Kind: `syntax`
- Lines: 221-221
- Attributes: `function`, `total`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  syntax Bool ::= isPrime(Int) [function, total]
```

### verification.k:222:1776f9d075f4

- Kind: `rule`
- Lines: 222-222
- Attributes: none
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule isPrime(N:Int) => trialPrime(N, 2, N >=Int 2)
```

### verification.k:224:c8b1c5b024ac

- Kind: `syntax`
- Lines: 224-224
- Attributes: `function`, `total`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  syntax Int ::= largestPrime(IntList, Int) [function, total]
```

### verification.k:225:f13f02acb542

- Kind: `rule`
- Lines: 225-225
- Attributes: none
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule largestPrime(.IntList, CUR:Int) => CUR
```

### verification.k:226:870d4b3a7010

- Kind: `rule`
- Lines: 226-229
- Attributes: `simplification`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule largestPrime(intCons(N:Int, IS:IntList), CUR:Int)
    => largestPrime(IS, N)
    requires N >Int CUR andBool isPrime(N)
    [simplification]
```

### verification.k:230:3ae921d844ad

- Kind: `rule`
- Lines: 230-234
- Attributes: `simplification`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule largestPrime(intCons(N:Int, IS:IntList), CUR:Int)
    => largestPrime(IS, CUR)
    requires N <=Int CUR
      orBool (N >Int CUR andBool notBool isPrime(N))
    [simplification]
```

### verification.k:236:975a1ae82d17

- Kind: `syntax`
- Lines: 236-236
- Attributes: `function`, `total`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  syntax Int ::= digitAcc(Int, Int) [function, total]
```

### verification.k:237:f7fe0adeec4c

- Kind: `rule`
- Lines: 237-239
- Attributes: `simplification`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule digitAcc(N:Int, A:Int) => A
    requires N <=Int 0
    [simplification]
```

### verification.k:240:a68fea49f247

- Kind: `rule`
- Lines: 240-245
- Attributes: `simplification`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule digitAcc(N:Int, A:Int)
    => digitAcc(
         (N -Int pyMod(N, 10)) /Int 10,
         A +Int pyMod(N, 10))
    requires N >Int 0
    [simplification]
```

### verification.k:247:bdc89de79852

- Kind: `syntax`
- Lines: 247-247
- Attributes: `function`, `total`
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  syntax Int ::= digitSum(Int) [function, total]
```

### verification.k:248:190e15cb842f

- Kind: `rule`
- Lines: 248-250
- Attributes: none
- Decision: `SOUND_DEFINITIONAL_SUMMARY`
- Rationale: Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.

```k
  rule digitSum(N:Int) => digitAcc(N, 0)

  // Exact AST fragments emitted by py2mpy.py for solution.py.
```

### verification.k:251:4da3c1b1fc90

- Kind: `syntax`
- Lines: 251-251
- Attributes: `macro`
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  syntax Expr ::= "#primeCond" [macro]
```

### verification.k:252:650a2e311d94

- Kind: `rule`
- Lines: 252-257
- Attributes: none
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  rule #primeCond => BoolOp(
    "and",
    Name("prime"),
    Compare(
      BinOp("*", Name("divisor"), Name("divisor")),
      CmpOp("<=", Name("number"))))
```

### verification.k:259:50da5de302af

- Kind: `syntax`
- Lines: 259-259
- Attributes: `macro`
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  syntax Stmts ::= "#primeBody" [macro]
```

### verification.k:260:11907e6f0e71

- Kind: `rule`
- Lines: 260-266
- Attributes: none
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  rule #primeBody =>
    If(Compare(
      BinOp("%", Name("number"), Name("divisor")),
      CmpOp("==", Int(0))),
      Assign(Name("prime"), Bool(false)),
      .Stmts)
    AugAssign(Name("divisor"), "+", Int(1))
```

### verification.k:268:68157323c2b2

- Kind: `syntax`
- Lines: 268-268
- Attributes: `macro`
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  syntax Stmts ::= "#scanBody" [macro]
```

### verification.k:269:8435a6bf41b8

- Kind: `rule`
- Lines: 269-279
- Attributes: none
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  rule #scanBody =>
    If(Compare(Name("number"), CmpOp(">", Name("largest"))),
      Assign(Name("divisor"), Int(2))
      Assign(
        Name("prime"),
        Compare(Name("number"), CmpOp(">=", Int(2))))
      While(#primeCond, #primeBody)
      If(Name("prime"),
        Assign(Name("largest"), Name("number")),
        .Stmts),
      .Stmts)
```

### verification.k:281:ee32d22c06e4

- Kind: `syntax`
- Lines: 281-281
- Attributes: `macro`
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  syntax Expr ::= "#digitCond" [macro]
```

### verification.k:282:998b8ee7721f

- Kind: `rule`
- Lines: 282-283
- Attributes: none
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  rule #digitCond =>
    Compare(Name("largest"), CmpOp(">", Int(0)))
```

### verification.k:285:cebef39b6f53

- Kind: `syntax`
- Lines: 285-285
- Attributes: `macro`
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  syntax Stmts ::= "#digitBody" [macro]
```

### verification.k:286:5007c2812940

- Kind: `rule`
- Lines: 286-291
- Attributes: none
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  rule #digitBody =>
    AugAssign(
      Name("digit_total"),
      "+",
      BinOp("%", Name("largest"), Int(10)))
    AugAssign(Name("largest"), "//", Int(10))
```

### verification.k:293:e720d13a3f69

- Kind: `syntax`
- Lines: 293-293
- Attributes: `macro`
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  syntax Stmts ::= "#functionBody" [macro]
```

### verification.k:294:893069bd9c22

- Kind: `rule`
- Lines: 294-306
- Attributes: none
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  rule #functionBody =>
    Assign(Name("largest"), Int(0))
    Assign(Name("number"), Int(0))
    Assign(Name("divisor"), Int(2))
    Assign(Name("prime"), Bool(false))
    Assign(Name("digit_total"), Int(0))
    For(Name("number"), Name("lst"), #scanBody)
    While(#digitCond, #digitBody)
    Return(Name("digit_total"))

  // Bounded entry-prefix summary.  It is the direct composition of MPY-CALL's
  // frame allocation, #bindP, the five literal assignments, and For's
  // one-time iterable evaluation.  No loop iteration is summarized here.
```

### verification.k:307:3690f6a2fbc7

- Kind: `rule`
- Lines: 307-339
- Attributes: `priority(37)`
- Decision: `OPERATIONAL_BRIDGE_EVIDENCE_GAP`
- Rationale: Exact bounded prefix for the immutable body by static composition, but no bridge-free universal K connection theorem is supplied.

```k
  rule <k>
         #applyK(
           toCall(closureVal(
             ("lst", .ParamNames),
             #functionBody,
             0)),
           (list(asVals(IS:IntList)), .Vals))
        =>
         #loop(list(asVals(IS)), Name("number"), #scanBody)
         ~> While(#digitCond, #digitBody)
         ~> Return(Name("digit_total"))
         ~> #endcall
       </k>
       <env> 0 => 1 </env>
       <scopes>
         MOD:Map
         =>
         MOD
         1 |-> scope(
           ("lst" |-> list(asVals(IS)))
           ("largest" |-> 0)
           ("number" |-> 0)
           ("divisor" |-> 2)
           ("prime" |-> false)
           ("digit_total" |-> 0),
           parent(0))
       </scopes>
       <scopeLoc> 1 => 2 </scopeLoc>
       <stack>
         .List => ListItem(frame(.K, 0, 1))
       </stack>
       requires notBool (1 in_keys(MOD))
       [priority(37)]
```

### verification.k:341:a3c0a217cc58

- Kind: `syntax`
- Lines: 341-341
- Attributes: `macro`
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  syntax Module ::= "solutionModule" [macro]
```

### verification.k:342:03d798e4ba3d

- Kind: `rule`
- Lines: 342-343
- Attributes: none
- Decision: `EXACT_MACRO`
- Rationale: AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.

```k
  rule solutionModule =>
    Module(FuncDef("skjkasdkd", Params("lst"), #functionBody))
```

### verification.k:344:4c5df27adc71

- Kind: `endmodule`
- Lines: 344-344
- Attributes: none
- Decision: `STRUCTURE`
- Rationale: Module/import structure.

```k
endmodule
```

### spec.k:1:570d3928c063

- Kind: `requires`
- Lines: 1-1
- Attributes: none
- Decision: `SPEC_STRUCTURE`
- Rationale: Specification module structure or imports.

```k
requires "verification.k"
```

### spec.k:3:c6567408bb5c

- Kind: `module`
- Lines: 3-3
- Attributes: none
- Decision: `SPEC_STRUCTURE`
- Rationale: Specification module structure or imports.

```k
module SPEC
```

### spec.k:4:2b51e5207d6d

- Kind: `imports`
- Lines: 4-6
- Attributes: none
- Decision: `SPEC_STRUCTURE`
- Rationale: Specification module structure or imports.

```k
  imports VERIFICATION

  // Trial-division loop invariant.
```

### spec.k:7:39cb9d171f5f

- Kind: `claim`
- Lines: 7-41
- Attributes: none
- Decision: `POSITIVE_REACHABILITY_CLAIM`
- Rationale: Reconstructed independently; dependency-ordered command exited 0 with #Top.

```k
  claim [prime-loop]:
    <k> #while(#primeCond, #primeBody) ~> K:K
      => K
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        ("number" |-> N:Int)
        ("divisor" |-> D:Int)
        ("prime" |-> B:Bool)
        REST:Map,
        P:Parent)
      =>
      SC
      L |-> scope(
        ("number" |-> N)
        ("divisor" |-> trialDivisor(N, D, B))
        ("prime" |-> trialPrime(N, D, B))
        REST,
        P)
    </scopes>
    requires D >=Int 2
      andBool (notBool B orBool N >=Int 2)
      andBool notBool ("number" in_keys(REST))
      andBool notBool ("divisor" in_keys(REST))
      andBool notBool ("prime" in_keys(REST))
      andBool notBool ("$cells" in_keys(REST))
      andBool notBool ("$cells" in_keys(
        ("number" |-> N)
        ("divisor" |-> D)
        ("prime" |-> B)
        REST))

  // Decimal digit accumulation loop invariant.
```

### spec.k:42:1fb409da7c9d

- Kind: `claim`
- Lines: 42-72
- Attributes: none
- Decision: `POSITIVE_REACHABILITY_CLAIM`
- Rationale: Reconstructed independently; dependency-ordered command exited 0 with #Top.

```k
  claim [digit-loop]:
    <k> #while(#digitCond, #digitBody) ~> K:K
      => K
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        ("largest" |-> N:Int)
        ("digit_total" |-> A:Int)
        REST:Map,
        P:Parent)
      =>
      SC
      L |-> scope(
        ("largest" |-> 0)
        ("digit_total" |-> digitAcc(N, A))
        REST,
        P)
    </scopes>
    requires N >=Int 0
      andBool notBool ("largest" in_keys(REST))
      andBool notBool ("digit_total" in_keys(REST))
      andBool notBool ("$cells" in_keys(REST))
      andBool notBool ("$cells" in_keys(
        ("largest" |-> N)
        ("digit_total" |-> A)
        REST))

  // The list-loop invariant includes the fixed suffix of the function.  On
  // completion it returns to the caller, so temporary locals are unobservable.
```

### spec.k:73:8fad87222174

- Kind: `claim`
- Lines: 73-117
- Attributes: none
- Decision: `POSITIVE_REACHABILITY_CLAIM`
- Rationale: Reconstructed independently; dependency-ordered command exited 0 with #Top.

```k
  claim [scan-loop]:
    <k>
      #loop(list(asVals(IS:IntList)), Name("number"), #scanBody)
      ~> While(#digitCond, #digitBody)
      ~> Return(Name("digit_total"))
      ~> #endcall
      => digitSum(largestPrime(IS, CUR)) ~> CONT:K
    </k>
    <env> S:Int => CALLER:Int </env>
    <scopes>
      BASE:Map
      S |-> scope(
        ("largest" |-> CUR:Int)
        ("number" |-> OLDN:Int)
        ("divisor" |-> OLDD:Int)
        ("prime" |-> OLDB:Bool)
        ("digit_total" |-> 0)
        REST:Map,
        parent(0))
      => BASE
    </scopes>
    <scopeLoc> S +Int 1 => S </scopeLoc>
    <stack>
      ListItem(frame(CONT, CALLER, S)) STACK:List
      => STACK
    </stack>
    <ret> noRet </ret>
    requires CUR >=Int 0
      andBool notBool ("largest" in_keys(REST))
      andBool notBool ("number" in_keys(REST))
      andBool notBool ("divisor" in_keys(REST))
      andBool notBool ("prime" in_keys(REST))
      andBool notBool ("digit_total" in_keys(REST))
      andBool notBool ("$cells" in_keys(REST))
      andBool notBool ("$cells" in_keys(
        ("largest" |-> CUR)
        ("number" |-> OLDN)
        ("divisor" |-> OLDD)
        ("prime" |-> OLDB)
        ("digit_total" |-> 0)
        REST))
      andBool notBool (S in_keys(BASE))

  // Function-call theorem.  The bounded entry prefix reaches scan-loop; the
  // proven scan-loop invariant then discharges the unbounded computation.
```

### spec.k:118:9313d1512779

- Kind: `claim`
- Lines: 118-137
- Attributes: none
- Decision: `POSITIVE_REACHABILITY_CLAIM`
- Rationale: Reconstructed independently; dependency-ordered command exited 0 with #Top.

```k
  claim [entry-prefix]:
    <k>
      #applyK(
        toCall(closureVal(
          ("lst", .ParamNames),
          #functionBody,
          0)),
        (list(asVals(IS:IntList)), .Vals))
      => digitSum(largestPrime(IS, 0))
    </k>
    <env> 0 </env>
    <scopes> MOD:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires notBool (1 in_keys(MOD))

  // End-to-end theorem: the translated function, loaded into the supplied
  // Python semantics, returns the digit sum of the largest prime in any
  // integer list (or zero when no prime exists).
```

### spec.k:138:1ce49a190f16

- Kind: `claim`
- Lines: 138-163
- Attributes: none
- Decision: `POSITIVE_REACHABILITY_CLAIM`
- Rationale: Reconstructed independently; dependency-ordered command exited 0 with #Top.

```k
  claim [main-correct]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("skjkasdkd"), (list(asVals(IS:IntList)), .Exprs))
      => digitSum(largestPrime(IS, 0))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "skjkasdkd" |-> closureVal(
          ("lst", .ParamNames),
          #functionBody,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
```

### spec.k:164:4c5df27adc71

- Kind: `endmodule`
- Lines: 164-164
- Attributes: none
- Decision: `SPEC_STRUCTURE`
- Rationale: Specification module structure or imports.

```k
endmodule
```
