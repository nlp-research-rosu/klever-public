requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports UNIQUE-VERIFICATION

  claim [member-summary-vacuity-support]:
    <k>
      #memberAcc(V:Val, list(VS:ValSeq)) ~> CONT:K
      => memberVS(V, VS) ~> CONT
    </k>

  claim [unique-loop-vacuity-support]:
    <k>
      #loop(list(INPUT:ValSeq), Name("item"), uniqueLoopBody) ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        .Map
          [ "l" <- ARG:Val ]
          [ "result" <- ref(H) ]
          [ "item" <- OLD:Val => lastItem(INPUT, OLD) ],
        parent(P:Int)) ...
    </scopes>
    <heap>
      ... H:Int |-> list(ACC:ValSeq => uniqueAcc(INPUT, ACC)) ...
    </heap>

  // Deliberately false result mutation.  For INPUT=.ValSeq, the real returned
  // list is empty, not [999].
  claim [unique-false-result]:
    <k>
      #loadAll(
        Module(
          FuncDef("unique", Params("l"), uniqueBody)
          Assign(
            Name("answer"),
            Call(Name("unique"), list(INPUT:ValSeq)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        .Map
          [ "unique" <- closureVal("l", uniqueBody, 0) ]
          [ "answer" <- ref(1) ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(uniqueAcc(INPUT, .ValSeq))
      1 |-> list(vCons(999, sortVS(uniqueAcc(INPUT, .ValSeq))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
