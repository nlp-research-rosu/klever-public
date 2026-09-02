# Claim meanings and satisfiable witnesses

## `encode-total`

Precondition: `<k>` directly calls a closure whose one parameter is `message`,
whose body is the exact submitted function body, whose defining scope is `0`,
and whose argument is `str(INPUT)`. The module scope is empty with the trusted
builtins parent, all allocation stores are empty/fresh, the call stack is empty,
and return/exception/exit state is normal. There is no side condition on
`INPUT`.

Postcondition: the call returns exactly `str(encodeCodes(INPUT))`; every other
listed cell is unchanged. This is an equality-constraining destination, not an
implication or a free result.

Satisfying state: choose `INPUT = .IntSeq` (or the code sequence for `"test"`)
and the ground cells shown in the claim.

## `encode-init`

Precondition: the same realizable direct-closure call state as `encode-total`.

Postcondition: ordinary call setup and the three initialization assignments
have reached the real `#loop`; environment `1` contains the original message,
empty result/char strings, and integer code `0`; the continuation is the real
return statement followed by `#endcall`, and the exact caller frame is on the
stack.

Satisfying state: choose `INPUT = .IntSeq` and the ground initial cells in the
claim.

## `encode-loop`

Precondition: execution is at the real string-loop head with arbitrary remaining
`INPUT`, accumulator `ACC`, and old local values; the exact return/endcall
continuation and frame are present. The loop body never reads `_MESSAGE`,
`_OLDCHAR`, or `_OLDCODE` before overwriting the latter two, so this deliberate
generalization does not skip behavior.

Postcondition: execution returns exactly `str(encodeAcc(INPUT, ACC))`, removes
the callee scope/frame, restores environment `0` and allocation location `1`,
and leaves heap, return, exception, and exit state normal.

Satisfying state: `INPUT` is the code sequence for `"test"`, `ACC` is the code
sequence for `"P"`, `_MESSAGE = INPUT`, `_OLDCHAR = .IntSeq`, and `_OLDCODE = 0`,
with all other cells exactly as in the claim. The expected result is `"PTGST"`.
