requires "body-mutant-verification.k"

module PILE-BODY-MUTANT-SPEC
  imports PILE-VERIFICATION-MUTANT

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
      0 |-> scope(MODULE:Map, parent(-1))
      1 |-> scope(
        ("n" |-> N:Int)
        ("stones" |-> ref(0))
        ("i" |-> I:Int),
        parent(0))
    =>
      -1 |-> BUILTINS
      0 |-> scope(MODULE, parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      0 |-> list(VS:ValSeq)
    =>
      0 |-> list(valSeqConcat(VS, pile(N, I)))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires
      N >Int 0
      andBool I >=Int 0
      andBool I <=Int N
endmodule
