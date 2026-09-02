requires "verification.k"

module AUDIT-FRESH-FALSE-RESULT
  imports VERIFICATION

  // Satisfying input ["x", "yyyy", "zz"] has true result "yyyy".
  // The destination is deliberately mutated to the false result "zz".
  claim [false-final-result]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List", "Optional")
        FuncDef(
          "longest",
          Params("strings"),
          If(
            UnaryOp("not", Name("strings")),
            Return(NoneVal),
            .Stmts
          )
          Assign(Name("result"), Subscript(Name("strings"), Int(0)))
          Assign(Name("string"), Name("result"))
          For(
            Name("string"),
            Name("strings"),
            If(
              Compare(
                Call(Name("len"), Name("string")),
                CmpOp(">", Call(Name("len"), Name("result")))
              ),
              Assign(Name("result"), Name("string")),
              .Stmts
            )
          )
          Return(Name("result"))
        )
      ))
      ~> Call(
           Name("longest"),
           list(
             vCons(
               str(iCons(120, .IntSeq)),
               vCons(
                 str(iCons(121, iCons(121, iCons(121, iCons(121, .IntSeq))))),
                 vCons(str(iCons(122, iCons(122, .IntSeq))), .ValSeq)
               )
             )
           )
         )
      => str(iCons(122, iCons(122, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?_FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
