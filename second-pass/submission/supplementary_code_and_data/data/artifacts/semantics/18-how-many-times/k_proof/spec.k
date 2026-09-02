requires "verification.k"

module HOW-MANY-TIMES-SPEC
  imports HOW-MANY-TIMES-VERIFICATION

  // Inductive invariant for the tail-recursive verification machine.
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

  // The translated Python closure implements the mathematical contract in
  // every surrounding machine state satisfying the normal fresh-frame
  // invariant.
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
      overlapCount(S, P) ~> CONT
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
