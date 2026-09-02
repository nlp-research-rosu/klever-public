requires "verification.k"

module SPEC-ENTRY-ONLY-AUDIT
  imports VERIFICATION

  claim [entry-true-without-helper-claims]:
    <k>
      Call(
        Name("has_close_elements"),
        (list(vCons(A:Float, vCons(B:Float, .ValSeq))), T:Float))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(
          "has_close_elements" |-> targetClosure,
          parent(-1))
      ) => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires floatLt(absF(subF(A, B)), T)
endmodule
