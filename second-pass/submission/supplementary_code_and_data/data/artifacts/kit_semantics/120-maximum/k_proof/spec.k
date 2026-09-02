requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [maximum-correct]:
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
      Call(Name("maximum"), list(VS:ValSeq), K:Int)
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
      0 |-> list(sortVS(VS))
      1 |-> maximumResult(VS, K)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 1 <=Int vsLen(VS)
     andBool vsLen(VS) <=Int 1000
     andBool 0 <=Int K
     andBool K <=Int vsLen(VS)
endmodule
