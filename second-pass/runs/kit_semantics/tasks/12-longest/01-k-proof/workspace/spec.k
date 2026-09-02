requires "verification.k"

module SPEC
  imports VERIFICATION

  // Circularity for the source for-loop. It is symbolic in the entire
  // remaining ValSeq, so it covers every finite input length.
  claim [loop-invariant]:
    <k>
      #loop(
        list(REST:ValSeq),
        Name("string"),
        If(
          Compare(
            Call(Name("len"), Name("string")),
            CmpOp(">", Call(Name("len"), Name("result")))
          ),
          Assign(Name("result"), Name("string")),
          .Stmts
        )
      )
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(MODULE:Map, parent(-1))
      L |-> scope(
        "strings" |-> _ORIGINAL:Val
        "result"  |-> (ACC:Val => scanLongest(REST, ACC))
        "string"  |-> (CURRENT:Val => ?_LAST:Val),
        parent(0)
      )
    </scopes>
    requires allStrings(REST)
      andBool isStringValue(ACC)
      andBool isStringValue(CURRENT)
      andBool L =/=Int 0
      andBool L =/=Int -1
      andBool notBool ("len" in_keys(MODULE))

  claim [empty-input]:
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
      ~> Call(Name("longest"), list(.ValSeq))
      => noneV
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

  claim [nonempty-input]:
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
      ~> Call(Name("longest"), list(vCons(FIRST:Val, REST:ValSeq)))
      => longestValue(vCons(FIRST, REST))
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
    requires isStringValue(FIRST)
      andBool allStrings(REST)
endmodule
