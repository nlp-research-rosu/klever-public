# Verification notes

`MPY-BUILTINS` models `hashlib.md5(S).hexdigest()` as the trusted symbolic
value `str(md5hexCodes(S))`.  The declaration of `md5hexCodes` has
`[no-evaluators]`, and the supplied semantics explicitly provides no concrete
twin for it.

Accordingly, the LLVM checks in `prove.sh` do two things:

1. run the empty-input branch to completion and check that it binds `noneV`;
2. execute the prompt example up to the oracle boundary and check that the
   oracle receives the ASCII code sequence for `Hello world`.

Removing the depth bound from the second command makes the LLVM interpreter
exit 113 when it is asked to evaluate the deliberately opaque function.  The
Haskell proof does not approximate that call: it proves for every nonempty
symbolic code sequence `CS` that the implementation returns exactly the
reference value `str(md5hexCodes(CS))`.  A separate claim proves the empty
sequence returns `noneV`.
