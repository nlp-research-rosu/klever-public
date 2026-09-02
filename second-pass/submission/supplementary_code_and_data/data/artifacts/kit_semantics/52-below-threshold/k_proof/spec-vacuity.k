requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: below_threshold([5], 5) returns false, not true.
  claim [false-postcondition]:
    <k>
      #loadAll(
        Module(
          FuncDef("below_threshold", Params("l", "t"),
            Expr(Str("Return True if all numbers in the list l are below threshold t."))
            Assign(Name("e"), Int(0))
            For(Name("e"), Name("l"),
              If(Compare(Name("e"), CmpOp("<", Name("t"))),
                Continue, .Stmts)
              Return(Bool(false)))
            Return(Bool(true)))))
      ~> Call(Name("below_threshold"), list(vCons(5, .ValSeq)), 5)
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
