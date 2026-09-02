requires "verification.k"

module SPEC
  imports VERIFICATION

  // Base member of the loop-invariant family.
  claim [concat-loop-empty]:
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
      0 |-> scope(GLOBALS:Map, parent(-1))
      1 |-> scope(
        "result"  |-> str(ACC:IntSeq)
        "string"  |-> CURRENT:Val
        "strings" |-> list(ALL:ValSeq),
        parent(0)
      )
      =>
      -1 |-> builtinsScope
      0 |-> scope(GLOBALS, parent(-1))
      1 |-> scope(
        "result"  |-> str(ACC)
        "string"  |-> CURRENT
        "strings" |-> list(ALL),
        parent(0)
      )
    </scopes>

  // Inductive member: one real MPY iteration executes, then the invariant
  // applies to REST. The equality guard is exactly the List[str] head test.
  claim [concat-loop-step]:
    <k>
      #loop(
        list(vCons(HEAD:Val, REST:ValSeq)),
        Name("string"),
        AugAssign(Name("result"), "+", Name("string"))
      )
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(GLOBALS:Map, parent(-1))
      1 |-> scope(
        "result"  |-> str(ACC:IntSeq)
        "string"  |-> CURRENT:Val
        "strings" |-> list(ALL:ValSeq),
        parent(0)
      )
      =>
      -1 |-> builtinsScope
      0 |-> scope(GLOBALS, parent(-1))
      1 |-> scope(
        "result"  |-> str(concatFrom(ACC, vCons(HEAD, REST)))
        "string"  |-> lastFrom(CURRENT, vCons(HEAD, REST))
        "strings" |-> list(ALL),
        parent(0)
      )
    </scopes>
    requires HEAD ==K str(stringCodes(HEAD))
     andBool isStringSeq(REST)

  // Exact translated module load, binding, function body, call, and return.
  claim [concatenate]:
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
      ~> Call(Name("concatenate"), list(VS:ValSeq))
      => str(concatFrom(.IntSeq, VS))
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
    requires isStringSeq(VS)
endmodule
