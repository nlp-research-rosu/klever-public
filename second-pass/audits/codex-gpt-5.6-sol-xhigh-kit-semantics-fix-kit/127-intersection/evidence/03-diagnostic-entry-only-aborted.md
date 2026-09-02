The command recorded in `03-diagnostic-entry-only-aborted.log` selected only
the entry claim and therefore filtered out `SPEC.prime-loop`, the circularity
needed to summarize the submitted loop. The reviewer terminated that diagnostic
run after approximately six minutes; the containing process returned status
130. This is not a candidate proof failure and is not used as verdict evidence.

The required independent branch runs instead select the loop claim together
with one entry claim, so each entry is checked in isolation while retaining its
explicit auxiliary circularity.
