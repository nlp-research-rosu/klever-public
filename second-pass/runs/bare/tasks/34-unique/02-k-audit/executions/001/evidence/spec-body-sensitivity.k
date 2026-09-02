requires "candidate-source/verification.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  claim <k> apply(
          Module(FuncDef("unique", Params("l"),
            Return(Call(Name("set"), Name("l"))))),
          VList(L))
    => VList(uniqueSpec(L)) </k>
endmodule
