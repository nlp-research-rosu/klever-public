requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Deliberately false, satisfiable ground mutation: maximum([1,2], 1) is
  // [2], but the destination demands an empty result list.
  claim [false-ground-result-rejected]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "maximum",
            Params("arr", "k"),
            Return(
              Subscript(
                Call(Name("sorted"), Name("arr")),
                Slice(
                  BinOp("-", Call(Name("len"), Name("arr")), Name("k")),
                  NoBound,
                  NoBound))))))
      ~>
      Call(Name("maximum"), list(vCons(1, vCons(2, .ValSeq))), 1)
      =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
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
      0 |-> list(sortVS(vCons(1, vCons(2, .ValSeq))))
      1 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
