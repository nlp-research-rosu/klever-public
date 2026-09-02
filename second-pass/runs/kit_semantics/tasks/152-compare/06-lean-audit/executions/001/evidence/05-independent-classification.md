# Independent Stage 3 classification

Canonical local closure: `VERIFICATION` only. Its import `MPY` is supplied by
the required semantics and is not a module declared in `verification.k`.

## Per-rule judgment

1. `rule-29a9419a5013224a8657110320f5222d8360897d1c1ad05d5b21b9a8a070d15a`
   (lines 7-8): **DEFINITION**. This is the empty-left constructor equation
   of the named Boolean proof predicate `sameIntLists`. It says that an empty
   left sequence is admissible precisely when the right sequence is empty.

2. `rule-4c226b697298ea8f665e9c7a275c999f5ca1704cf1bffeda3ab4c575a950d681`
   (line 9): **DEFINITION**. This is the nonempty-left/empty-right constructor
   equation of `sameIntLists`, returning false for a length mismatch.

3. `rule-23a1b598b8aca7e64fdbbbdf6c2eba606e3434ffea5d8b33eb5ff9c67a39d82f`
   (lines 10-18): **DEFINITION**. This is the descending two-cons recurrence
   of `sameIntLists`. It names the proof-domain predicate: both heads must be
   unboxed integers with an unboxed subtraction result, and both tails must
   satisfy the predicate. Together with rules 1-2, its constructor cases are
   disjoint and cover all `ValSeq` pairs; that is appropriate for `[total]`.

4. `rule-35d6b10b3b07c6654b6990fa450ff659514b515f9afb5c4ddcd292c7a52a4d4e`
   (line 21): **DEFINITION**. This is the empty/empty base equation of the
   named result summary `compareAcc`; exhausted tails return the accumulated
   sequence.

5. `rule-b6a35c28b2d565d80431890d82ed0b37f41b8e521dd15d430123581b67f0d014`
   (lines 22-35): **DEFINITION**. This is the descending two-cons recurrence
   of `compareAcc`. It appends exactly `abs(score - predicted)` and recurs on
   both tails. It is deliberately partial for unequal tail lengths, while the
   claims use it under `sameIntLists`; this agrees with its non-`total`
   declaration.

## Operational-semantic cross-check

The source body iterates over `zip(game, guess)`, mutates `result` with
`append(abs(score - predicted))`, and returns it. In the frozen semantics,
`zip` yields paired heads and stops when either input is empty; `#loop` consumes
one yielded pair per iteration; integer subtraction is `I1 -Int I2`; `abs`
maps an integer through `absInt`; list `append` updates the heap using
`valSeqConcat(VS, vCons(V, .ValSeq))`. The `compareAcc` recurrence is therefore
the exact value recurrence used by the proved equal-length integer claims.

None of the five rules is an ordinary execution/observation rule: none matches
a `<k>` computation or replaces fixed execution. None was first proved as the
same rule in a module excluding it and then used later, so none is a
`PROVED_DERIVED_LEMMA`. None asserts a free-standing mathematical fact about
the result; they are constructor equations for named proof terms, so none is a
`DOMAIN_LEMMA`. All canonical attribute lists are empty, hence there are no
`simplification` rules to police and the independently reconstructed true
domain-lemma set is empty.
