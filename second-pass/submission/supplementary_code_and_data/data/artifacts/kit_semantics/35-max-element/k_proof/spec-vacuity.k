requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: max_element([1, 2]) is 2, not 1.  This also forces
  // the greater-than/replacement branch of the numeric fold.
  claim [false-result]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "max_element",
            Params("l"),
            Return(Call(Name("max"), Name("l")))
          )
        )
      )
      ~> Call(
           Name("max_element"),
           list(vCons(1, vCons(2, .ValSeq)))
         )
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "max_element" |->
          closureVal(
            ("l", .ParamNames),
            (Return(Call(Name("max"), Name("l"))) .Stmts),
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
endmodule

module SPEC-VACUITY-KEEP
  imports VERIFICATION

  // Deliberately false: max_element([2, 1]) keeps 2; returning 1 would take
  // the replacement branch when the comparison is false.
  claim [false-keep-result]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "max_element",
            Params("l"),
            Return(Call(Name("max"), Name("l")))
          )
        )
      )
      ~> Call(
           Name("max_element"),
           list(vCons(2, vCons(1, .ValSeq)))
         )
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "max_element" |->
          closureVal(
            ("l", .ParamNames),
            (Return(Call(Name("max"), Name("l"))) .Stmts),
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
endmodule
