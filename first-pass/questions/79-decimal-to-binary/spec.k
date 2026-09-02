// spec.k — decimal_to_binary, TRAP-FREE (P79). One straight-line entry claim;
// domain decimal >= 0 (the shared bin() guard).
//
//   kompile verification.k --backend haskell --main-module DECIMAL-TO-BINARY-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module DECIMAL-TO-BINARY-SPEC

requires "verification.k"

module DECIMAL-TO-BINARY-SPEC
  imports DECIMAL-TO-BINARY-VERIFICATION

  claim
    <k>
      FuncDef("decimal_to_binary", Params("decimal"),
        Return(BinOp("+",
          BinOp("+", Str("db"),
            Subscript(Call(Name("bin"), Name("decimal")), Slice(Int(2), NoBound, NoBound))),
          Str("db"))))
      Assign(Name("result"), Call(Name("decimal_to_binary"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "decimal_to_binary" <- ?_:Val ] [ "result" <- d2bRes(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [all-path]
endmodule
