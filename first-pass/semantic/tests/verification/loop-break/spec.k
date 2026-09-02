requires "verification.k"

module LOOP-BREAK-SPEC
  imports LOOP-BREAK-VERIFICATION

  // ---- Loop invariant (circularity): #loop(list(VS), x, body) => .K, total => prefixSum(VS, B).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("x"), CmpOp("<", Int(0))), Break, .Stmts)
        AugAssign(Name("total"), "+", Name("x")))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "xs" <- XSV:Val ] [ "x" <- _:Val ] [ "total" <- B:Int ], P:Parent) =>
        scope(.Map [ "xs" <- XSV ] [ "x" <- ?_:Val ] [ "total" <- ?T:Int ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?T ==Int prefixSum(VS, B)
    [all-path]

  // ---- Entry claim — result = f(list(VS)) == prefixSum(VS, 0).
  claim
    <k>
      FuncDef("f", Params("xs"),
        Assign(Name("total"), Int(0))
        For(Name("x"), Name("xs"),
          If(Compare(Name("x"), CmpOp("<", Int(0))), Break, .Stmts)
          AugAssign(Name("total"), "+", Name("x")))
        Return(Name("total")))
      Assign(Name("result"), Call(Name("f"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "f" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?R ==Int prefixSum(VS, 0)
    [all-path]
endmodule
