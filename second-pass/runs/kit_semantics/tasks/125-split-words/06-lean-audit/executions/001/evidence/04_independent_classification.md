# Independent Stage 3 semantic classification

The canonical local closure is only module `VERIFICATION`, with exactly two
rules. Neither rule has a `simplification` attribute.

1. `rule-f119e21...` (`verification.k:8-75`) is a `DEFINITION`. Its nullary
   `[function,total]` symbol `splitWordsBody : Stmts` expands to the complete
   constructor tree for the source function body: assignment of `txt.split()`,
   the whitespace branch, the comma branch, and the left-associated sum of the
   thirteen `count` calls. It neither matches a `<k>` cell nor skips an
   operational transition. The fixed call semantics subsequently binds and
   executes the expanded `Stmts`. This is a named proof term / macro-like AST
   definition, not an operational bridge or domain fact.

2. `rule-fe0451...` (`verification.k:80-93`) is a `DEFINITION`. Its sole,
   unconditional, nonrecursive equation defines the summary function
   `oddAlphabetCount(CS)` as the sum of `cntSub(CS,[98])`, ..., `cntSub(CS,[122])`.
   The source return expression independently executes thirteen string
   `count` method calls; fixed semantics maps each such call to the same
   `cntSub` recurrence (`semantics/methods.k:33-44`) and integer addition to
   `+Int` (`semantics/int.k:9`). Thus the equation names the result expression;
   it does not assert an independently meaningful theorem about an otherwise
   defined function and does not replace source execution.

There are no `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`
entries. `prove.sh` builds `verification.k` with both equations before its
single positive `kprove`; it contains no earlier proof of either exact rule in
a module from which the rule is absent. That confirms neither equation could
qualify as a proved-derived lemma, although both already meet the stronger,
more direct definitional classification.

The true domain-lemma set is therefore empty. The thirteen-letter summary is
material and relevant to the source postcondition, but its rule is a transparent
definition rather than an assumed domain equality.
