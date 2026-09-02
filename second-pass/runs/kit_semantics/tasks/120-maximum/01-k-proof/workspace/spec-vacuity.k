requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the realizable witness arr = [1, 2], k = 1:
  // the returned list is [2], not [].
  claim [false-result]:
    <k>
      Call(
        Name("maximum"),
        list(vCons(1, vCons(2, .ValSeq))),
        1)
      =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "maximum" |->
          closureVal(
            ("arr", "k"),
            Return(
              Subscript(
                Call(Name("sorted"), Name("arr")),
                Slice(
                  BinOp("-", Call(Name("len"), Name("arr")), Name("k")),
                  NoBound,
                  NoBound))),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(1, vCons(2, .ValSeq)))
      1 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
