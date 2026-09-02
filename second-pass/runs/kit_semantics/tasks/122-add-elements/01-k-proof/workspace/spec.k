requires "verification.k"

module SPEC
  imports VERIFICATION

  // Full entry theorem.  INPUT and K are symbolic; the constraints are exactly
  // the HumanEval material domain, including every length from 1 through 100.
  claim [add-elements]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "add_elements",
            Params("arr", "k"),
            Assign(Name("total"), Int(0))
            Assign(Name("element"), Int(0))
            Assign(Name("remaining"), Name("k"))
            For(
              Name("element"),
              Name("arr"),
              If(
                Compare(Name("remaining"), CmpOp("==", Int(0))),
                Break .Stmts,
                .Stmts
              )
              If(
                BoolOp(
                  "and",
                  Compare(Name("element"), CmpOp(">=", UnaryOp("-", Int(99)))),
                  Compare(Name("element"), CmpOp("<=", Int(99)))
                ),
                AugAssign(Name("total"), "+", Name("element")) .Stmts,
                .Stmts
              )
              AugAssign(Name("remaining"), "-", Int(1))
            )
            Return(Name("total"))
          )
        )
      )
      ~> Call(Name("add_elements"), list(INPUT:ValSeq), Int(K:Int))
      =>
      qualifyingPrefix(INPUT, K)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "add_elements" |->
          closureVal(
            ("arr", "k"),
            Assign(Name("total"), Int(0))
            Assign(Name("element"), Int(0))
            Assign(Name("remaining"), Name("k"))
            For(
              Name("element"),
              Name("arr"),
              If(
                Compare(Name("remaining"), CmpOp("==", Int(0))),
                Break .Stmts,
                .Stmts
              )
              If(
                BoolOp(
                  "and",
                  Compare(Name("element"), CmpOp(">=", UnaryOp("-", Int(99)))),
                  Compare(Name("element"), CmpOp("<=", Int(99)))
                ),
                AugAssign(Name("total"), "+", Name("element")) .Stmts,
                .Stmts
              )
              AugAssign(Name("remaining"), "-", Int(1))
            )
            Return(Name("total")),
            0
          ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(INPUT)
     andBool 1 <=Int vsLen(INPUT)
     andBool vsLen(INPUT) <=Int 100
     andBool 1 <=Int K
     andBool K <=Int vsLen(INPUT)
endmodule
