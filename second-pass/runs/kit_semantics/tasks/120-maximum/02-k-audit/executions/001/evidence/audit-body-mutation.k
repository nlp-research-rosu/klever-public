requires "verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Real loaded body changed from len(arr)-k to len(arr)-k-1, while the
  // original maximumResult obligation is retained. For [1,2], k=1 the
  // mutant returns [1,2], not [2].
  claim [mutated-loaded-body-rejected]:
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
                  BinOp(
                    "-",
                    BinOp("-", Call(Name("len"), Name("arr")), Name("k")),
                    Int(1)),
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
                  BinOp(
                    "-",
                    BinOp("-", Call(Name("len"), Name("arr")), Name("k")),
                    Int(1)),
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
      1 |-> maximumResult(vCons(1, vCons(2, .ValSeq)), 1)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
