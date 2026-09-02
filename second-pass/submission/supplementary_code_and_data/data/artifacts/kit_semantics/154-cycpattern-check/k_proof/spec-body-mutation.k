requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated body: it always returns false, so this true
  // postcondition for ("hello", "ell") must be rejected.
  claim [mutated-body]:
    <k>
      Call(
        Name("cycpattern_check"),
        Str("hello"),
        Str("ell"))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "cycpattern_check" |->
          closureVal(
            ("a", "b"),
            Return(Bool(false)),
            0),
        parent(-1))
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
