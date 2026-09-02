requires "verification.k"

module FRESH-BODY-SENSITIVITY
  imports VERIFICATION

  // The closure actually called below has a materially changed program body:
  // it always returns true. The real program returns false for ("abcd","abd"),
  // so preserving the real program's false postcondition must be rejected.
  claim [mutated-executed-body]:
    <k>
      Call(
        Name("cycpattern_check"),
        Str("abcd"),
        Str("abd"))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "cycpattern_check" |->
          closureVal(
            ("a", "b"),
            Return(Bool(true)),
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
