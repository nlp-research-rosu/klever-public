requires "verification.k"

module SPEC
  imports VERIFICATION

  // Exact execution theorem for the fixed list-membership fold.
  claim [member-fold]:
    <k> #memberAcc(V:Val, list(S:ValSeq))
      => commonMember(V, S) ... </k>

  // Loop invariant: A is the unprocessed suffix and ACC is the result so far.
  claim [common-loop]:
    <k>
      #loop(list(A:ValSeq), Name("item"), commonLoopBody())
      ~> (Return(Call(Name("sorted"), Name("result"))) .Stmts)
      ~> #endcall
    =>
      (Return(Call(Name("sorted"), Name("result"))) .Stmts)
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(GLOBALS:Map, parent(-1))
       1 |-> scope(
         "l1"     |-> list(ORIG:ValSeq)
         "l2"     |-> list(B:ValSeq)
         "result" |-> ref(0)
         "item"   |-> (ITEM:Val => ?FINALITEM:Val),
         parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(ACC:ValSeq => commonAcc(A, B, ACC)) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Whole program, including loading and executing the exact function body.
  claim [common-program]:
    <k>
      #loadAll(Module(
        FuncDef("common", Params("l1", "l2"), commonBody())
      ))
      ~> Call(Name("common"), list(A:ValSeq), list(B:ValSeq))
    =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0  |-> scope(
        "common" |-> closureVal(
          ("l1", "l2", .ParamNames),
          commonBody(),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(commonAcc(A, B, .ValSeq))
      1 |-> list(sortVS(commonAcc(A, B, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
