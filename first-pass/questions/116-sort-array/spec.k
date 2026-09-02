// spec.k — sort_array, TRAP-FREE (W3 P116). One entry claim: the REAL
// sorted(sorted(arr), key=<ones-count-of-bin lambda>) lands as
// sortKeyVS(sortVS(VS), <the closure verbatim>) (P145 shape; the lambda has
// no free vars, so it carries only its definition env index).
//
//   kompile verification.k --backend haskell --main-module SORT-ARRAY-BIN-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SORT-ARRAY-BIN-SPEC

requires "verification.k"

module SORT-ARRAY-BIN-SPEC
  imports SORT-ARRAY-BIN-VERIFICATION

  claim
    <k>
      FuncDef("sort_array", Params("arr"),
        Return(
          Call(
            Name("sorted"),
            Call(Name("sorted"), Name("arr")),
            KwArg(
              "key",
              Lambda(
                Params("x"),
                CellVars(.ParamNames),
                FreeVars(.ParamNames),
                Call(
                  Attribute(
                    Subscript(
                      Call(Name("bin"), Name("x")),
                      Slice(Int(2), NoBound, NoBound)),
                    "count"),
                  Str("1")))))))
      Assign(Name("result"), Call(Name("sort_array"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sort_array" <- ?_:Val ] [ "result" <- ref(?H:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map =>
      (?H |-> list(sortKeyVS(sortVS(VS),
        closureValC(("x", .ParamNames), .ParamNames,
          Return(Call(
            Attribute(
              Subscript(
                Call(Name("bin"), Name("x")),
                Slice(Int(2), NoBound, NoBound)),
              "count"),
            Str("1"))) .Stmts, .Map)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
