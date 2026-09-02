requires "reference-semantics/semantics.k"

module BF-VERIFICATION-BODY-MUTATED
  imports MPY

  // This is the exact AST emitted in solution.mpy, factored out only so that
  // the reachability claims can supply arbitrary arguments to a final call.
  syntax Stmts ::= "bfBody" [macro]
  rule bfBody
    => Assign(
         Name("planets"),
         TupleExpr(
           Str("Mercury"),
           Str("Venus"),
           Str("EarthX"),
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
         Name("first"),
         Call(Attribute(Name("planets"), "index"), Name("planet1")))
       Assign(
         Name("second"),
         Call(Attribute(Name("planets"), "index"), Name("planet2")))
       If(
         Compare(Name("first"), CmpOp("<", Name("second"))),
         Return(
           Subscript(
             Name("planets"),
             Slice(
               BinOp("+", Name("first"), Int(1)),
               Name("second"),
               NoBound))),
         .Stmts)
       Return(
         Subscript(
           Name("planets"),
           Slice(
             BinOp("+", Name("second"), Int(1)),
             Name("first"),
             NoBound)))

  syntax Module ::= "bfCall" "(" Expr "," Expr ")" [macro]
  rule bfCall(P1, P2)
    => Module(
         FuncDef("bf", Params("planet1", "planet2"), bfBody)
         Expr(Call(Name("bf"), P1, P2)))

  syntax Expr ::= "bfRun" "(" Expr "," Expr ")" [macro]
  rule bfRun(P1, P2)
    => Call(
         closureVal(
           "planet1", "planet2", .ParamNames,
           bfBody,
           0),
         P1,
         P2)

  // An independent mathematical form of the contract: take the open interval
  // between the two orbital positions from the canonical planet sequence.
  syntax ValSeq ::= "planetVals" [function, total]
  rule planetVals
    => vCons(str(strToCodes("Mercury")),
       vCons(str(strToCodes("Venus")),
       vCons(str(strToCodes("Earth")),
       vCons(str(strToCodes("Mars")),
       vCons(str(strToCodes("Jupiter")),
       vCons(str(strToCodes("Saturn")),
       vCons(str(strToCodes("Uranus")),
       vCons(str(strToCodes("Neptune")), .ValSeq))))))))

  syntax Val ::= expectedBetween(Int, Int) [function, total]
  rule expectedBetween(I, J)
    => doSlice(
         tuple(planetVals),
         someB(minInt(I, J) +Int 1),
         someB(maxInt(I, J)),
         noB)

  // A finite specification sort lets one symbolic claim quantify over all
  // 8 x 8 valid input pairs without treating arbitrary strings as planets.
  syntax Planet ::= "pMercury" | "pVenus" | "pEarth" | "pMars"
                  | "pJupiter" | "pSaturn" | "pUranus" | "pNeptune"

  syntax IntSeq ::= planetCodes(Planet) [function, total]
  rule planetCodes(pMercury) => strToCodes("Mercury")
  rule planetCodes(pVenus)   => strToCodes("Venus")
  rule planetCodes(pEarth)   => strToCodes("Earth")
  rule planetCodes(pMars)    => strToCodes("Mars")
  rule planetCodes(pJupiter) => strToCodes("Jupiter")
  rule planetCodes(pSaturn)  => strToCodes("Saturn")
  rule planetCodes(pUranus)  => strToCodes("Uranus")
  rule planetCodes(pNeptune) => strToCodes("Neptune")

  syntax Int ::= planetPosition(Planet) [function, total]
  rule planetPosition(pMercury) => 0
  rule planetPosition(pVenus)   => 1
  rule planetPosition(pEarth)   => 2
  rule planetPosition(pMars)    => 3
  rule planetPosition(pJupiter) => 4
  rule planetPosition(pSaturn)  => 5
  rule planetPosition(pUranus)  => 6
  rule planetPosition(pNeptune) => 7

  // Deterministically exercise every valid ordered pair.  Assert is part of
  // MPY: a wrong result changes <exc>/<exit-code>, so the reachability claim
  // below cannot close if even one of these 64 calls is wrong.
  syntax Expr ::= planetExpr(Int) [function]
  rule planetExpr(0) => Str("Mercury")
  rule planetExpr(1) => Str("Venus")
  rule planetExpr(2) => Str("Earth")
  rule planetExpr(3) => Str("Mars")
  rule planetExpr(4) => Str("Jupiter")
  rule planetExpr(5) => Str("Saturn")
  rule planetExpr(6) => Str("Uranus")
  rule planetExpr(7) => Str("Neptune")

  syntax KItem ::= #validCases(Int, Int)
  rule <k>
         #validCases(I, J)
       =>
         Assert(
           Compare(
             bfRun(planetExpr(I), planetExpr(J)),
             CmpOp("==", expectedBetween(I, J))))
         ~> #validCases(I, J +Int 1)
       ...
       </k>
    requires 0 <=Int I andBool I <=Int 7
     andBool 0 <=Int J andBool J <Int 7

  rule <k>
         #validCases(I, 7)
       =>
         Assert(
           Compare(
             bfRun(planetExpr(I), planetExpr(7)),
             CmpOp("==", expectedBetween(I, 7))))
         ~> #validCases(I +Int 1, 0)
       ...
       </k>
    requires 0 <=Int I andBool I <Int 7

  rule <k>
         #validCases(7, 7)
       =>
         Assert(
           Compare(
             bfRun(planetExpr(7), planetExpr(7)),
             CmpOp("==", expectedBetween(7, 7))))
       ...
       </k>
endmodule
