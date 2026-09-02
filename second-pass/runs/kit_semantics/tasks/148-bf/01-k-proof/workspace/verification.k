requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact statement body emitted in solution.mpy.  These two macro rules are
  // syntax abbreviations only: after macro expansion the fixed MPY rules
  // execute the real function definition, call, body, and return.
  syntax Stmts ::= "bfBody" [macro]
  rule bfBody =>
    Assign(
      Name("planets"),
      TupleExpr(
        Str("Mercury"),
        Str("Venus"),
        Str("Earth"),
        Str("Mars"),
        Str("Jupiter"),
        Str("Saturn"),
        Str("Uranus"),
        Str("Neptune")))
    If(
      BoolOp(
        "or",
        Compare(Name("planet1"), CmpOp("not in", Name("planets"))),
        Compare(Name("planet2"), CmpOp("not in", Name("planets")))),
      Return(TupleExpr(.Exprs)),
      .Stmts)
    Assign(
      Name("index1"),
      Call(Attribute(Name("planets"), "index"), Name("planet1")))
    Assign(
      Name("index2"),
      Call(Attribute(Name("planets"), "index"), Name("planet2")))
    If(
      Compare(Name("index1"), CmpOp("<", Name("index2"))),
      Return(
        Subscript(
          Name("planets"),
          Slice(
            BinOp("+", Name("index1"), Int(1)),
            Name("index2"),
            NoBound))),
      .Stmts)
    Return(
      Subscript(
        Name("planets"),
        Slice(
          BinOp("+", Name("index2"), Int(1)),
          Name("index1"),
          NoBound)))

  syntax Module ::= "bfModule" [macro]
  rule bfModule =>
    Module(FuncDef("bf", Params("planet1", "planet2"), bfBody))

  syntax Expr ::= bfCall(IntSeq, IntSeq) [macro]
  rule bfCall(P1, P2) =>
    Call(Name("bf"), str(P1), str(P2))

  // Mathematical model of the ordered planet names.
  syntax ValSeq ::= "planetValues" [function, total]
  rule planetValues =>
    vCons(str(strToCodes("Mercury")),
    vCons(str(strToCodes("Venus")),
    vCons(str(strToCodes("Earth")),
    vCons(str(strToCodes("Mars")),
    vCons(str(strToCodes("Jupiter")),
    vCons(str(strToCodes("Saturn")),
    vCons(str(strToCodes("Uranus")),
    vCons(str(strToCodes("Neptune")), .ValSeq))))))))

  // -1 means that the supplied string is not a planet name.
  syntax Int ::= planetIndex(IntSeq) [function, total]
  rule planetIndex(P) => 0 requires P ==K strToCodes("Mercury")
  rule planetIndex(P) => 1 requires P ==K strToCodes("Venus")
  rule planetIndex(P) => 2 requires P ==K strToCodes("Earth")
  rule planetIndex(P) => 3 requires P ==K strToCodes("Mars")
  rule planetIndex(P) => 4 requires P ==K strToCodes("Jupiter")
  rule planetIndex(P) => 5 requires P ==K strToCodes("Saturn")
  rule planetIndex(P) => 6 requires P ==K strToCodes("Uranus")
  rule planetIndex(P) => 7 requires P ==K strToCodes("Neptune")
  rule planetIndex(P) => -1
    requires notBool (P ==K strToCodes("Mercury"))
     andBool notBool (P ==K strToCodes("Venus"))
     andBool notBool (P ==K strToCodes("Earth"))
     andBool notBool (P ==K strToCodes("Mars"))
     andBool notBool (P ==K strToCodes("Jupiter"))
     andBool notBool (P ==K strToCodes("Saturn"))
     andBool notBool (P ==K strToCodes("Uranus"))
     andBool notBool (P ==K strToCodes("Neptune"))

  syntax ValSeq ::= betweenPlanets(IntSeq, IntSeq) [function, total]
  rule betweenPlanets(P1, P2) =>
    betweenIndices(planetIndex(P1), planetIndex(P2))

  syntax ValSeq ::= betweenIndices(Int, Int) [function, total]
  rule betweenIndices(I, J) => .ValSeq
    requires I <Int 0 orBool J <Int 0
  rule betweenIndices(I, J) => buildVS(planetValues, I +Int 1, J, 1)
    requires I >=Int 0 andBool J >=Int 0 andBool I <Int J
  rule betweenIndices(I, J) => buildVS(planetValues, J +Int 1, I, 1)
    requires I >=Int 0 andBool J >=Int 0 andBool I >=Int J
endmodule
