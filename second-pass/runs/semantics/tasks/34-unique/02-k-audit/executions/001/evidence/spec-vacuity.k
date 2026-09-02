requires "spec.k"

module UNIQUE-SPEC-VACUITY
  imports UNIQUE-SPEC

  // False witness: for the satisfying input [1], the result is [1], not [].
  // This changes only the result-bearing heap object in the entry postcondition.
  claim [unique-correct-false-empty]:
    <k>
      #loadAll(
        Module(
          FuncDef("unique", Params("l"), uniqueBody)
          Assign(
            Name("answer"),
            Call(Name("unique"), list(vCons(1, .ValSeq))))))
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
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
