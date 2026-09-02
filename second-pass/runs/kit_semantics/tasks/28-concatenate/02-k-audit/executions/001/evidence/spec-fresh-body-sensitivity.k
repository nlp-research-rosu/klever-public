requires "verification.k"

module SPEC-FRESH-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed body is materially changed: it appends "x", not the element.
  // On the satisfying input ["a"] the mutant returns "x", so "a" must be rejected.
  claim [changed-executed-body]:
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
              AugAssign(Name("result"), "+", Str("x"))
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
