# Ground precondition witnesses

These substitutions make every positive claim source pattern and `requires`
clause satisfiable.

- `SHAPE-CONNECTION-SPEC.for-list-shape`: `T = Name("value")`,
  `V = list(.ValSeq)`, and `B = .Stmts`. Then
  `rowContents(V) = .ValSeq`, so the guard is
  `list(.ValSeq) ==K list(.ValSeq)`.
- `SPEC.inner-loop`: `VS = .ValSeq`, `L = 1`, `OUT = 9`, `CI = 0`,
  `SC = .Map`, `LST = list(.ValSeq)`, `ROW = list(.ValSeq)`, `RI = 0`,
  `_OLD = 0`, `X = 1`, `ACC = .ValSeq`, and `H = .Map`. All named map
  entries are then ground and the loop is the empty-list loop.
- `SPEC.outer-loop`: `RS = .ValSeq`, `L = 1`, `OUT = 9`, `_CI = 0`,
  `SC = .Map`, `LST = list(.ValSeq)`, `_OLDROW = noneV`, `RI = 0`,
  `_OLDVALUE = 0`, `X = 1`, `ACC = .ValSeq`, and `H = .Map`.
  `listRows(.ValSeq)` rewrites to `true`.
- `SPEC.column-key`: `RI = 2` and `CI = 3`, with the other cells exactly
  ground as displayed in the claim.
- `SPEC.row-key`: `RI = 2` and `CI = 3`, with the other cells exactly ground
  as displayed in the claim.
- `SPEC.get-row`: the simplest witness is `RS = .ValSeq` and `X = 1`; its
  exact displayed environment, scopes, empty heap, and other ground cells
  complete the state, and `listRows(.ValSeq)` is `true`. A nonempty witness
  used for result substitution is
  `RS = [[2,1,2],[2],[1,2,1,2]]` in Python notation and `X = 2`; its exact
  K encoding and matching Python results are recorded in
  `stage4-concrete-witness.log`.
