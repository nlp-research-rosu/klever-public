requires "verification.k"

module SPEC
  imports VERIFICATION

  claim <k> apply(
          Module(FuncDef("unique", Params("l"),
            Return(Call(Name("sorted"), Call(Name("set"), Name("l")))))),
          VList(L))
    => VList(uniqueSpec(L)) </k>

  claim <k> run(
          Module(FuncDef("unique", Params("l"),
            Return(Call(Name("sorted"), Call(Name("set"), Name("l")))))),
          ListExpr(Int(5), Int(3), Int(5), Int(2), Int(3), Int(3),
                   Int(9), Int(0), Int(123)))
    => VList(ListItem(VInt(0)) ListItem(VInt(2)) ListItem(VInt(3))
             ListItem(VInt(5)) ListItem(VInt(9)) ListItem(VInt(123))) </k>
endmodule
