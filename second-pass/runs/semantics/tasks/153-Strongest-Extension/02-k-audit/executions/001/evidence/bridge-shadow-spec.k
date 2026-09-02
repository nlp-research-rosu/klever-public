requires "/tmp/audit-work/reconstruction/verification.k"

module BRIDGE-SHADOW-SPEC
  imports STRONGEST-EXTENSION-VERIFICATION

  // In this satisfiable state, normal lexical lookup selects the local shadow
  // that returns 99.  The proof-local Call bridge ignores that binding.
  claim
    <k>
      Call(Name("_extension_strength"), Name("x"))
    =>
      99
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        ("x" |-> str(iCons(65, .IntSeq)))
        ("_extension_strength" |->
          closureVal(
            ("extension", .ParamNames),
            Return(Int(99)) .Stmts,
            1)),
        parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(shadow-fixed-result)]

  claim
    <k>
      Call(Name("_extension_strength"), Name("x"))
    =>
      1
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (1 |-> scope(
        ("x" |-> str(iCons(65, .IntSeq)))
        ("_extension_strength" |->
          closureVal(
            ("extension", .ParamNames),
            Return(Int(99)) .Stmts,
            1)),
        parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(shadow-fabricated-strength)]
endmodule
