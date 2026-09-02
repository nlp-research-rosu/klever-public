// spec.k — the reachability claim kprove discharges. On the UNIFIED semantics.
//
//   kompile verification.k --backend haskell \
//     --main-module COUNT-DISTINCT-CHARACTERS-VERIFICATION \
//     --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled \
//     --spec-module COUNT-DISTINCT-CHARACTERS-SPEC

requires "verification.k"

module COUNT-DISTINCT-CHARACTERS-SPEC
  imports COUNT-DISTINCT-CHARACTERS-VERIFICATION

  // ---- Entry claim — see ./PROOF.md ----------------------------------------
  // count_distinct_characters is a PURE nested expression (no loop): the three builtins
  // .lower() / set() / len() fire once each on the symbolic str(CS), composing to
  //   isLen(dedupCodes(mapLower(CS))) = distinctCount(CS).
  // After `result = count_distinct_characters(str(CS))` the root scope's result is
  // distinctCount(CS): the number of distinct characters of CS, case-insensitively.
  // Holds for ANY symbolic code-sequence CS (no domain restriction — the function is total).
  claim
    <k>
      FuncDef("count_distinct_characters", Params("string"),
        Return(
          Call(Name("len"),
            Call(Name("set"),
              Call(Attribute(Name("string"), "lower"), .Exprs)))))
      Assign(Name("result"),
        Call(Name("count_distinct_characters"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "count_distinct_characters" <- ?_:Val ]
                       [ "result" <- distinctCount(CS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
