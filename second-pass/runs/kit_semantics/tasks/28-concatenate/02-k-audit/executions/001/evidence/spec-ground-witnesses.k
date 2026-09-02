requires "verification.k"

module SPEC-GROUND-WITNESSES
  imports VERIFICATION

  claim [loop-empty-witness]:
    <k>
      #loop(
        list(.ValSeq),
        Name("string"),
        AugAssign(Name("result"), "+", Name("string"))
      )
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "result"  |-> str(iCons(97, iCons(98, .IntSeq)))
        "string"  |-> str(iCons(122, .IntSeq))
        "strings" |-> list(.ValSeq),
        parent(0)
      )
      =>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "result"  |-> str(iCons(97, iCons(98, .IntSeq)))
        "string"  |-> str(iCons(122, .IntSeq))
        "strings" |-> list(.ValSeq),
        parent(0)
      )
    </scopes>

  claim [loop-step-witness]:
    <k>
      #loop(
        list(vCons(str(iCons(99, .IntSeq)), .ValSeq)),
        Name("string"),
        AugAssign(Name("result"), "+", Name("string"))
      )
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "result"  |-> str(iCons(97, iCons(98, .IntSeq)))
        "string"  |-> str(iCons(122, .IntSeq))
        "strings" |-> list(vCons(str(iCons(99, .IntSeq)), .ValSeq)),
        parent(0)
      )
      =>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "result"  |-> str(iCons(97, iCons(98, iCons(99, .IntSeq))))
        "string"  |-> str(iCons(99, .IntSeq))
        "strings" |-> list(vCons(str(iCons(99, .IntSeq)), .ValSeq)),
        parent(0)
      )
    </scopes>

  claim [entry-empty-witness]:
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
      ~> Call(Name("concatenate"), list(.ValSeq))
      => str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?EMPTYSCOPES:Map
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>

  claim [entry-single-witness]:
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
        list(vCons(str(iCons(113, .IntSeq)), .ValSeq))
      )
      => str(iCons(113, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?SINGLESCOPES:Map
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>

  claim [entry-mixed-witness]:
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
            str(.IntSeq),
            vCons(
              str(iCons(97, iCons(98, .IntSeq))),
              vCons(str(iCons(99, .IntSeq)), .ValSeq)
            )
          )
        )
      )
      => str(iCons(97, iCons(98, iCons(99, .IntSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?MIXEDSCOPES:Map
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
