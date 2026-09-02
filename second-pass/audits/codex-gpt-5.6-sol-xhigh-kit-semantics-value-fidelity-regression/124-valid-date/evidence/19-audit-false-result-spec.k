requires "verification.k"

module AUDIT-FALSE-RESULT-SPEC
  imports VERIFICATION

  // Fresh reviewer mutation: 02-29-0000 is valid under the explicit
  // February-1-through-29 contract, but this claim deliberately requires false.
  claim [false-february-29-result]:
    <k> Call(
          Name("valid_date"),
          (str(iCons(48,
               iCons(50,
               iCons(45,
               iCons(50,
               iCons(57,
               iCons(45,
               iCons(48,
               iCons(48,
               iCons(48,
               iCons(48, .IntSeq))))))))))), .Exprs))
        => false
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("valid_date" |-> validDateClosure, parent(-1))
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
