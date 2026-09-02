requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately changed body: it appends "" instead of the loop element.
  // For ["a"] this mutant returns "", so the original "a" result must fail.
  claim [changed-body]:
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
              AugAssign(Name("result"), "+", Str(""))
            )
            Return(Name("result"))
          )
        )
      )
      ~> Call(
        Name("concatenate"),
        list(vCons(str(iCons(97, .IntSeq)), .ValSeq))
      )
      => str(iCons(97, .IntSeq))
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
