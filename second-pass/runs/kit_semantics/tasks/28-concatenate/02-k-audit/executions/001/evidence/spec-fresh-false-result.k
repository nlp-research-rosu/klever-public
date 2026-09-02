requires "verification.k"

module SPEC-FRESH-FALSE-RESULT
  imports VERIFICATION

  // The real program returns "ab" on ["a", "b"]; "ac" is a fresh false result.
  claim [false-result-ab-to-ac]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef(
            "concatenate",
            Params("strings"),
            Assign(Name("result"), Str(""))
            Assign(Name("string"), Str(""))
            For(
              Name("string"),
              Name("strings"),
              AugAssign(Name("result"), "+", Name("string"))
            )
            Return(Name("result"))
          )
        )
      )
      ~> Call(
        Name("concatenate"),
        list(
          vCons(
            str(iCons(97, .IntSeq)),
            vCons(str(iCons(98, .IntSeq)), .ValSeq)
          )
        )
      )
      => str(iCons(97, iCons(99, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
