requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Bool ::= freshScopes(Int, Map) [function]
  rule freshScopes(_:Int, .Map) => true
  rule L:Int in_keys(S:Map) => false
    requires freshScopes(L, S)
  rule freshScopes(N:Int, (L:Int |-> _:Scope) S:Map) => true
    requires N ==Int L +Int 1 andBool freshScopes(L, S)

  rule S:Map [ L:Int <- V:Scope ] => (L |-> V) S
    requires notBool L in_keys(S)
  rule ((L:Int |-> V:Scope) S:Map) [ L <- undef ] => S
    requires notBool L in_keys(S)

  syntax Stmts ::= "changeBaseBody" [function]
  rule changeBaseBody =>
    Expr(
      Str(
        "Change numerical base of input number x to base.\n    return string representation after the conversion.\n    base numbers are less than 10.\n    >>> change_base(8, 3)\n    '22'\n    >>> change_base(8, 2)\n    '1000'\n    >>> change_base(7, 2)\n    '111'\n    "))
    If(Compare(Name("x"), CmpOp("==", Int(0))),
      Return(Str("")),
      .Stmts)
    Return(
      BinOp(
        "+",
        Call(
          Name("change_base"),
          BinOp("//", Name("x"), Name("base")),
          Name("base")),
        Call(
          Name("chr"),
          BinOp(
            "+",
            Int(49),
            BinOp("%", Name("x"), Name("base"))))))

  syntax Module ::= "solutionModule" [function]
  rule solutionModule =>
    Module(
      FuncDef("change_base", Params("x", "base"),
        changeBaseBody))

  syntax Val ::= "changeBaseClosure" [function]
  rule changeBaseClosure =>
    closureVal(("x", "base", .ParamNames), changeBaseBody, 0)

  syntax IntSeq ::= baseDigits(Int, Int) [function]
  rule baseDigits(0, _:Int) => .IntSeq [simplification]
  rule baseDigits(N:Int, B:Int)
    => seqConcat(
         baseDigits((N -Int pyMod(N, B)) /Int B, B),
         iCons(48 +Int pyMod(N, B), .IntSeq))
    requires N >Int 0 andBool B >=Int 2
    [simplification]
endmodule
