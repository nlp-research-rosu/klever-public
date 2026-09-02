requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated body: the real (3, 4, 5) postcondition is retained,
  // but this body always returns false.
  claim [mutated-body-is-detected]:
    <k>
      Call(Name("right_angle_triangle"), 3, 4, 5)
      =>
      ?RESULT:Bool
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |->
          closureVal(
            ("a", "b", "c"),
            Return(Bool(false)),
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
    ensures ?RESULT ==Bool true
endmodule
