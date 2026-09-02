requires "verification.k"

module MAXIMUM-SPEC-VACUITY
  imports MAXIMUM-VERIFICATION

  // Deliberately false result mutation: append an extra zero to the result.
  // Satisfying witness L = [1], K = 1:
  //   real/claimed result = [1], mutated result = [1, 0].
  claim
    <k>
      Module(
        FuncDef("maximum", Params("arr", "k"),
          Return(
            Subscript(
              Call(Name("sorted"), Name("arr")),
              Slice(
                BinOp("-", Call(Name("len"), Name("arr")), Name("k")),
                NoBound,
                NoBound)))))
      ~> boot
      => .K
    </k>
    <args> ListItem(listVal(L:List)) ListItem(intVal(K:Int)) </args>
    <env> .Map => ("arr" |-> listVal(L)) ("k" |-> intVal(K)) </env>
    <out>
      noResult
      => listVal(maximumSpec(L, K) ListItem(0))
    </out>
  requires (0 <=Int K) andBool (K <=Int size(L))
endmodule
