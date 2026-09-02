# Invalid filtered-claim diagnostic

Two exploratory commands selected only `SPEC.triples-correct` or only
`SPEC.program-correct` with `--claims`. That filtering also removed the
preceding circularities on which each selected claim depends, so the commands
unrolled recursion instead of testing the candidate's dependency-preserving
proof. They were abandoned and are not proof evidence. Their command headers
are retained in `invalid-filter-triples-correct.log` and
`invalid-filter-program-correct.log`.

The valid independent runs are:

- `kprove-pair-correct.log`: pair claim alone;
- `kprove-pair-and-triples.log`: pair and triples claims together, excluding
  only the program claim; and
- `kprove-all-positive.log`: all three claims together, including every
  needed circularity.
