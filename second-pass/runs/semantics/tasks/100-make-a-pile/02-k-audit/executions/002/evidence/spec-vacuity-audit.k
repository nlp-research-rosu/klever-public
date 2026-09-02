requires "verification.k"

module PILE-AUDIT-VACUITY-SPEC
  imports PILE-VERIFICATION

  // Deliberately false result obligation: execution begins at index I and
  // appends that element, but this postcondition omits it by using I+1.
  // Witness N=3, I=0, VS=.ValSeq: actual [3,5,7], mutated [5,7].
  claim
    <k>
      #while(pileCondition, pileLoopBody)
      ~> (Return(Name("stones")) .Stmts):Stmts
      ~> #endcall
    =>
      ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> BUILTINS:Scope
      0 |-> scope(
        MODULE:Map,
        parent(-1))
      1 |-> scope(
        ("n" |-> N:Int)
        ("stones" |-> ref(0))
        ("i" |-> I:Int),
        parent(0))
    =>
      -1 |-> BUILTINS
      0 |-> scope(
        MODULE,
        parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      0 |-> list(VS:ValSeq)
    =>
      0 |-> list(
        valSeqConcat(
          VS,
          pile(N, I +Int 1)))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires
      N >Int 0
      andBool I >=Int 0
      andBool I <Int N
endmodule
