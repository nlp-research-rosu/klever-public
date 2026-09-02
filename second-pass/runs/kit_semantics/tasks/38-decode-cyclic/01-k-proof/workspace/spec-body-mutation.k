requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The result-building expression is deliberately changed from C+A+B to
  // A+B+C. The unchanged expected result must therefore be rejected.
  claim [changed-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "decode_cyclic",
            Params("s"),
            Expr(
              Str(
                "\n    Takes a string encoded by rotating each complete three-character group\n    left once, and restores the original string.\n    "))
            Assign(Name("result"), Str(""))
            Assign(Name("group"), Str(""))
            Assign(Name("char"), Str(""))
            For(
              Name("char"),
              Name("s"),
              Assign(
                Name("group"),
                BinOp("+", Name("group"), Name("char")))
              If(
                Compare(
                  Call(Name("len"), Name("group")),
                  CmpOp("==", Int(3))),
                Assign(
                  Name("result"),
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      Name("result"),
                      Subscript(
                        Name("group"),
                        Slice(NoBound, Int(2), NoBound))),
                    Subscript(Name("group"), Int(2))))
                Assign(Name("group"), Str("")),
                .Stmts))
            Return(BinOp("+", Name("result"), Name("group"))))))
      ~> Call(
           Name("decode_cyclic"),
           str(iCons(98, iCons(99, iCons(97, .IntSeq)))))
      => str(iCons(97, iCons(98, iCons(99, .IntSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "decode_cyclic" |-> ?FUN:Val, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
