requires "verification.k"

module GCD-SPEC-VACUITY
  imports GCD-VERIFICATION

  // Fresh reviewer mutation: the real submitted program returns 1 for (3, 5),
  // so changing its exact result to 2 must leave an unmet proof obligation.
  claim
    <k>
      #loadAll(Module(GcdDef .Stmts))
      ~> Call(Name("greatest_common_divisor"), (3, 5, .Exprs))
      => 2
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope("greatest_common_divisor" |-> GcdClosure,
                   parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <stack> .List </stack>
    <ret> noRet </ret>
    [label(false-result)]
endmodule
