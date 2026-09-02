requires "/tmp/audit-work/fresh/verification.k"

module HOW-MANY-TIMES-SPEC-VACUITY-AUDIT
  imports HOW-MANY-TIMES-VERIFICATION

  // Preserve the candidate's genuine helper obligation.
  claim
    <k>
      #overlapAcc(
        S:IntSeq,
        iCons(PC:Int, PS:IntSeq),
        A:Int)
      ~> CONT:K
    =>
      (A +Int overlapCount(S, iCons(PC, PS))) ~> CONT
    </k>

  // Fresh false mutation: every result is required to be one too large.
  claim
    <k>
      #applyK(
        toCall(
          closureVal(
            ("string", "substring"),
            howManyTimesBody,
            0)),
        (str(S:IntSeq), str(P:IntSeq), .Vals))
      ~> CONT:K
    =>
      (overlapCount(S, P) +Int 1) ~> CONT
    </k>
    <env> CALLER:Int </env>
    <scopes>
      0 |-> scope(
             ("how_many_times"
               |-> closureVal(
                     ("string", "substring"),
                     howManyTimesBody,
                     0))
             MODULE:Map,
             parent(-1))
      -1 |-> builtinsScope
      REST:Map
    </scopes>
    <scopeLoc> NEXT:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPNEXT:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool
      NEXT in_keys(
        (0 |-> scope(
                ("how_many_times"
                  |-> closureVal(
                        ("string", "substring"),
                        howManyTimesBody,
                        0))
                MODULE,
                parent(-1)))
        (-1 |-> builtinsScope)
        REST)
endmodule
