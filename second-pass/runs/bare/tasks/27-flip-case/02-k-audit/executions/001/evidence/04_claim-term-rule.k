rule Module(
       FuncDef("flip_case", Params("string"),
         Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))))
  => Module(
       FuncDef("flip_case", Params("string"),
         Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))))
