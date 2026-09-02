requires "verification.k"

module LOOP-GROUND-WITNESS
  imports VOWELS-BASE

  claim [loop-precondition-is-satisfiable]:
    <k>
      #loop(
        str(
          iCons(
            97,
            iCons(99, iCons(101, iCons(100, iCons(121, .IntSeq))))
          )
        ),
        Name("char"),
        vowelLoopBody
      )
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "s" |-> str(
          iCons(65, iCons(67, iCons(69, iCons(68, iCons(89, .IntSeq)))))
        )
        "count" |-> 2
        "char" |-> str(.IntSeq)
        "last_y" |-> false,
        parent(0)
      )
      =>
      1 |-> scope(
        "s" |-> str(
          iCons(65, iCons(67, iCons(69, iCons(68, iCons(89, .IntSeq)))))
        )
        "count" |-> 4
        "char" |-> str(iCons(121, .IntSeq))
        "last_y" |-> true,
        parent(0)
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module MAIN-GROUND-WITNESS
  imports VOWELS-VERIFICATION

  claim [main-precondition-is-satisfiable]:
    <k>
      #loadAll(vowelsModule)
      ~> Call(
        Name("vowels_count"),
        str(iCons(65, iCons(67, iCons(69, iCons(68, iCons(89, .IntSeq)))))
      )
      )
      =>
      3
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
        "vowels_count" |-> closureVal("s", vowelsBody, 0),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
