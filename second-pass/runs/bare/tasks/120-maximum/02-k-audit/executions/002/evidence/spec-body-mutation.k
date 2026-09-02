requires "verification.k"

module MAXIMUM-BODY-MUTATION
  imports MAXIMUM-VERIFICATION

  // The actual executed claim term is changed: the slice now begins at
  // len(arr) - len(arr), so it returns the full sorted list for every K.
  claim
    <k>
      Module(
        FuncDef("maximum", Params("arr", "k"),
          Return(
            Subscript(
              Call(Name("sorted"), Name("arr")),
              Slice(
                BinOp(
                  "-",
                  Call(Name("len"), Name("arr")),
                  Call(Name("len"), Name("arr"))),
                NoBound,
                NoBound)))))
      ~> boot
      => .K
    </k>
    <args> ListItem(listVal(L:List)) ListItem(intVal(K:Int)) </args>
    <env> .Map => ("arr" |-> listVal(L)) ("k" |-> intVal(K)) </env>
    <out> noResult => listVal(maximumSpec(L, K)) </out>
  requires (0 <=Int K) andBool (K <=Int size(L))
endmodule
