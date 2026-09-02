requires "verification.k"

module DIGITSUM-SPEC
  imports DIGITSUM-VERIFICATION

  // ---- Loop invariant (circularity) — single-accumulator value-predicate fold over
  // the string's codes CS. From result=R the loop leaves result := R +Int digSum(CS).
  // Induction on CS; ord(c) yields the code, the nested If splits on 65..90.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("code"), Call(Name("ord"), Name("c")))
        If(Compare(Name("code"), CmpOp(">=", Int(65))),
          If(Compare(Name("code"), CmpOp("<=", Int(90))),
            Assign(Name("result"), BinOp("+", Name("result"), Name("code"))),
            .Stmts),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "digitSum" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "result" <- R:Int ] [ "c" <- _:Val ] [ "code" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "s" <- SV ] [ "result" <- ?R2:Int ]
                   [ "c" <- ?_:Val ] [ "code" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R2 ==Int R +Int digSum(CS)
    [all-path]

  // ---- Entry claim — result = digitSum(str(CS)) == digSum(CS).
  claim
    <k>
      FuncDef("digitSum", Params("s"),
        Assign(Name("result"), Int(0))
        Assign(Name("c"), Str(""))
        For(Name("c"), Name("s"),
          Assign(Name("code"), Call(Name("ord"), Name("c")))
          If(Compare(Name("code"), CmpOp(">=", Int(65))),
            If(Compare(Name("code"), CmpOp("<=", Int(90))),
              Assign(Name("result"), BinOp("+", Name("result"), Name("code"))),
              .Stmts),
            .Stmts))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("digitSum"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "digitSum" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Int digSum(CS)
    [all-path]
endmodule
