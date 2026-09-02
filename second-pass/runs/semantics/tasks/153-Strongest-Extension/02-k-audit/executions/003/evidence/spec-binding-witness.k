requires "verification.k"

module BINDING-WITNESS-SPEC
  imports STRONGEST-EXTENSION-VERIFICATION

  // The local binding deliberately shadows the submitted helper with a
  // function returning 999. Fixed semantics must respect that binding.
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
            Return(Int(999)),
            0)),
        parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(binding-witness)]
endmodule
