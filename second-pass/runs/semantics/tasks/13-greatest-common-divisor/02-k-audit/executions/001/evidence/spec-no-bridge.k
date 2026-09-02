requires "verification-no-bridge.k"

module GCD-SPEC-NO-BRIDGE
  imports GCD-VERIFICATION-NO-BRIDGE

  claim
    <k>
      #loadAll(Module(GcdDef .Stmts))
      ~> Call(Name("greatest_common_divisor"),
              (A0:Int, B0:Int, .Exprs))
      => gcdSpec(absInt(A0), absInt(B0))
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
    [label(program-correct-no-bridge)]
endmodule
