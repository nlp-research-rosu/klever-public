requires "verification.k"

module MAXIMUM-SPEC-VACUITY-FRESH
  imports MAXIMUM-VERIFICATION

  // Fresh false result obligation.  The unchanged program is required to
  // return [], which is false for the satisfying witness L=[5], K=1.
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
    <out> noResult => listVal(.List) </out>
  requires (0 <=Int K) andBool (K <=Int size(L))
endmodule
