# Filtered-entry diagnostic

After the clean all-claims run and isolated `SPEC.prime-loop` run had both
exited 0 with `#Top`, the reviewer also invoked:

```text
kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC --claims SPEC.is-prime
```

This deliberately filters out the auxiliary loop circularity on which the
symbolic entry proof depends. It produced no output and continued unrolling
the unrestricted symbolic loop, so the reviewer interrupted it with SIGINT
after roughly two minutes. The tool session reported exit 130. This was a
diagnostic, not a required target run and not evidence of a failed candidate
claim. The valid entry target is the all-claims run, where K checks both the
loop circularity and its dependent entry theorem; the loop claim was also
checked separately.
