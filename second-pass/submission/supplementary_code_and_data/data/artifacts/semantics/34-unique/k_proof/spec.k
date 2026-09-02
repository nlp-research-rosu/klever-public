requires "verification.k"

module UNIQUE-SPEC
  imports UNIQUE-VERIFICATION

  claim [member-summary]:
    <k>
      #memberAcc(V:Val, list(VS:ValSeq)) ~> CONT:K
      => memberVS(V, VS) ~> CONT
    </k>

  claim [unique-loop]:
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
  claim [unique-correct]:
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
      1 |-> list(sortVS(uniqueAcc(INPUT, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
