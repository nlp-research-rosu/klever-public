requires "verification.k"

module GROUND-WITNESS-SPEC
  imports UNIQUE-VERIFICATION

  // Satisfying input [2, 1, 2, 3, 1].  The accumulator preserves first
  // occurrences [2, 1, 3], while the returned answer is [1, 2, 3].
  claim [ground-entry]:
    <k>
      #loadAll(
        Module(
          FuncDef("unique", Params("l"), uniqueBody)
          Assign(
            Name("answer"),
            Call(
              Name("unique"),
              list(
                vCons(
                  2,
                  vCons(1, vCons(2, vCons(3, vCons(1, .ValSeq))))))))))
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
      0 |-> list(vCons(2, vCons(1, vCons(3, .ValSeq))))
      1 |-> list(vCons(1, vCons(2, vCons(3, .ValSeq))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
