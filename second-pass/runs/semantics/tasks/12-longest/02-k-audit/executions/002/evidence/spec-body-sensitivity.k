requires "verification.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // Material body mutation: when "ab" is longer than current best "x", the
  // mutated loop still retains "x". The true destination remains "ab".
  claim
    <k>
      (#loop(
        list(stringVals(sCons(
          iCons(97, iCons(98, .IntSeq)),
          .StringSeq))),
        Name("string"),
        Assign(Name("result"), Name("result")))
      ~> Return(Name("result"))
      ~> #endcall)
      => (str(iCons(97, iCons(98, .IntSeq))) ~> .K)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope("longest" |-> longestSolution, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         "strings" |-> list(stringVals(sCons(
           iCons(97, iCons(98, .IntSeq)),
           .StringSeq)))
         "result" |-> str(iCons(120, .IntSeq))
         "string" |-> noneV,
         parent(0))
      => 0 |-> scope("longest" |-> longestSolution, parent(-1))
         -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(mutated-body-must-return-ab)]
endmodule
