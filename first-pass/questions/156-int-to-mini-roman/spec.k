// spec.k — int_to_mini_roman on the UNIFIED semantics (src/). A single straight-line entry claim (the
// closed form has no loop). See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module INT-TO-MINI-ROMAN-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module INT-TO-MINI-ROMAN-SPEC

requires "verification.k"

module INT-TO-MINI-ROMAN-SPEC
  imports INT-TO-MINI-ROMAN-VERIFICATION

  // ---- Entry — result = int_to_mini_roman(N) == romanRes(N): M[n//1000] + H[(n//100)%10] +
  // T[(n//10)%10] + U[n%10], the closed-form lowercase mini-Roman numeral. Domain 1 <= N <= 1000 (every
  // place index is then in range, thousands in {0,1}). The four table lookups concat via the str-+ bridge.
  claim
    <k>
      FuncDef("int_to_mini_roman", Params("number"),
        Assign(Name("M"), ListExpr(Str(""), Str("m")))
        Assign(Name("H"),
          ListExpr(Str(""), Str("c"), Str("cc"), Str("ccc"), Str("cd"), Str("d"),
                   Str("dc"), Str("dcc"), Str("dccc"), Str("cm")))
        Assign(Name("T"),
          ListExpr(Str(""), Str("x"), Str("xx"), Str("xxx"), Str("xl"), Str("l"),
                   Str("lx"), Str("lxx"), Str("lxxx"), Str("xc")))
        Assign(Name("U"),
          ListExpr(Str(""), Str("i"), Str("ii"), Str("iii"), Str("iv"), Str("v"),
                   Str("vi"), Str("vii"), Str("viii"), Str("ix")))
        Return(
          BinOp("+",
            BinOp("+",
              BinOp("+",
                Subscript(Name("M"), BinOp("//", Name("number"), Int(1000))),
                Subscript(Name("H"), BinOp("%", BinOp("//", Name("number"), Int(100)), Int(10)))),
              Subscript(Name("T"), BinOp("%", BinOp("//", Name("number"), Int(10)), Int(10)))),
            Subscript(Name("U"), BinOp("%", Name("number"), Int(10))))))
      Assign(Name("result"), Call(Name("int_to_mini_roman"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "int_to_mini_roman" <- ?_:Val ] [ "result" <- romanRes(N) ], parent(-1))
    </scopes>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1 andBool N <=Int 1000
    [all-path]
endmodule
