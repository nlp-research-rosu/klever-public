requires "verification.k"

module DOUBLE-DIFF-SPEC
  imports DOUBLE-DIFF-VERIFICATION

  // ---- Loop invariant (circularity) — value-predicate fold. From result=R the loop
  // leaves result := R +Int ddiff(VS). Induction on VS; nested If splits on e>0 then e%2.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("e"),
        If(Compare(Name("e"), CmpOp(">", Int(0))),
          If(Compare(BinOp("%", Name("e"), Int(2)), CmpOp("==", Int(1))),
            Assign(Name("result"), BinOp("+", Name("result"), BinOp("*", Name("e"), Name("e")))),
            .Stmts),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "lst" <- LV:Val ] [ "result" <- R:Int ] [ "e" <- _:Val ], P:Parent) =>
        scope(.Map [ "lst" <- LV ] [ "result" <- ?R2:Int ] [ "e" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?R2 ==Int R +Int ddiff(intListOf(VS))
    [all-path]

  // ---- Entry claim — result = double_the_difference(list(VS)) == ddiff(intListOf(VS)).
  claim
    <k>
      FuncDef("double_the_difference", Params("lst"),
        Assign(Name("result"), Int(0))
        Assign(Name("e"), Int(0))
        For(Name("e"), Name("lst"),
          If(Compare(Name("e"), CmpOp(">", Int(0))),
            If(Compare(BinOp("%", Name("e"), Int(2)), CmpOp("==", Int(1))),
              Assign(Name("result"), BinOp("+", Name("result"), BinOp("*", Name("e"), Name("e")))),
              .Stmts),
            .Stmts))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("double_the_difference"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "double_the_difference" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?R ==Int ddiff(intListOf(VS))
    [all-path]
endmodule
