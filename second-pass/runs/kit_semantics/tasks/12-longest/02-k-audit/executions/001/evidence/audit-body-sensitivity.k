requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  claim [mutated-source-body]:
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
                CmpOp("<", Call(Name("len"), Name("result")))
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
               str(iCons(97, .IntSeq)),
               vCons(str(iCons(98, iCons(98, .IntSeq))), .ValSeq)
             )
           )
         )
      => str(iCons(98, iCons(98, .IntSeq)))
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
