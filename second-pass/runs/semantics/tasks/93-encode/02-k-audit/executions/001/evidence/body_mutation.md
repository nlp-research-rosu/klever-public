# Body-sensitivity mutation

The scratch-only copy of `verification.k` changes the real loop-body expression
`chr(code + 2)` to `chr(code + 3)` while leaving `encodeCode` and all
postconditions unchanged. A proof that is sensitive to execution of the pinned
body must reject the original claims after this change.
