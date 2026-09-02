requires "/tmp/audit-work/fresh/verification.k"

module HOW-MANY-TIMES-BRIDGE-WRONG-BINDING-AUDIT
  imports HOW-MANY-TIMES-VERIFICATION

  // The directly supplied closure is valid, but its captured scope deliberately
  // binds the recursive name to integer 0. Fixed execution cannot recurse.
  claim
    <k>
      #applyK(
        toCall(
          closureVal(
            ("string", "substring"),
            howManyTimesBody,
            0)),
        (str(iCons(97, .IntSeq)),
         str(iCons(97, .IntSeq)),
         .Vals))
    =>
      1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("how_many_times" |-> 0, parent(-1))
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
