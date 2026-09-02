requires "verification-body-mutation.k"

module GROUND-BODY-MUTATION-SPEC
  imports UNIQUE-VERIFICATION-BODY-MUTATION

  // The unchanged expected result is false after the mutated body returns the
  // accumulator directly (and therefore performs no second allocation).
  claim [ground-body-mutation]:
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
