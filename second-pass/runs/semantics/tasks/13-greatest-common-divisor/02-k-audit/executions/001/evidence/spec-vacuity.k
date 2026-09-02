requires "verification.k"

module GCD-SPEC-VACUITY
  imports GCD-VERIFICATION

  // Deliberately false: for the satisfying witness A0=25, B0=15, the real
  // submitted program and gcdSpec both return 5, while this demands 6.
  claim
    <k>
      #loadAll(Module(GcdDef .Stmts))
      ~> Call(Name("greatest_common_divisor"),
              (A0:Int, B0:Int, .Exprs))
      => gcdSpec(absInt(A0), absInt(B0)) +Int 1
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
    [label(false-off-by-one)]
endmodule
