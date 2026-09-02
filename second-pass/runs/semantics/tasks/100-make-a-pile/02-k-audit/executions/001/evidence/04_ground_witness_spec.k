requires "verification.k"

module PILE-GROUND-ENTRY-SPEC
  imports PILE-VERIFICATION

  // Satisfying entry witness N=3, proved to the concrete returned heap list.
  claim
    <k>
      #loadAll(pileModule)
      ~> Call(Name("make_a_pile"), Int(3))
    =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> BUILTINS:Scope
    =>
      -1 |-> BUILTINS
      0 |-> scope(
        "make_a_pile" |-> pileClosure,
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(
        vCons(3,
          vCons(5,
            vCons(7, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule

module PILE-GROUND-LOOP-WITNESS-SPEC
  imports PILE-VERIFICATION

  // Satisfying loop witness N=3, I=1, VS=[3].
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
        ("n" |-> 3)
        ("stones" |-> ref(0))
        ("i" |-> 1),
        parent(0))
    =>
      -1 |-> BUILTINS
      0 |-> scope(MODULE, parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      0 |-> list(vCons(3, .ValSeq))
    =>
      0 |-> list(
        vCons(3,
          vCons(5,
            vCons(7, .ValSeq))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
