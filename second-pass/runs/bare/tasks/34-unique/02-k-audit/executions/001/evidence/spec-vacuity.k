requires "candidate-source/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: for the satisfying witness L = .List, this demands
  // [0] even though both Python implementations and the K semantics return [].
  claim <k> apply(
          Module(FuncDef("unique", Params("l"),
            Return(Call(Name("sorted"), Call(Name("set"), Name("l")))))),
          VList(L))
    => VList(ListItem(VInt(0)) uniqueSpec(L)) </k>
endmodule
