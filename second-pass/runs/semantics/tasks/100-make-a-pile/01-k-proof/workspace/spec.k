requires "verification.k"

module PILE-LOOP-SPEC
  imports PILE-VERIFICATION

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
          pile(N, I)))
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

module PILE-PREFIX-SPEC
  imports PILE-VERIFICATION

  claim
    <k>
      #loadAll(pileModule)
      ~> Call(Name("make_a_pile"), Int(N:Int))
    =>
      #while(pileCondition, pileLoopBody)
      ~> (Return(Name("stones")) .Stmts):Stmts
      ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> BUILTINS:Scope
    =>
      -1 |-> BUILTINS
      0 |-> scope(
        ?MODULE:Map,
        parent(-1))
      1 |-> scope(
        ("n" |-> N)
        ("stones" |-> ref(0))
        ("i" |-> 0),
        parent(0))
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack>
      .List => ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires N >Int 0
endmodule
