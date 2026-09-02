requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports FLOAT-SYNTAX

  // A proof-domain representation of every finite list of numeric
  // coefficients.  Its embedding is the actual ValSeq consumed by MPY.
  syntax NumSeq ::= ".NumSeq"
                  | nInt(Int, NumSeq)
                  | nFloat(Float, NumSeq)

  syntax ValSeq ::= numVals(NumSeq) [function, total]
  syntax Int ::= numLen(NumSeq) [function, total]
  syntax Bool ::= lastNonZero(NumSeq) [function, total]
  syntax Bool ::= validCoeffs(NumSeq) [function, total]

  // Exact, non-operational abbreviations for the translated source syntax.
  syntax Stmts ::= "polyStep" [function, total]
                 | "polyBody" [function, total]
                 | "expandBody" [function, total]
                 | "bisectBody" [function, total]
                 | "findZeroBody" [function, total]
  syntax Expr ::= "expandCond" [function, total]
                | "bisectCond" [function, total]
  syntax Module ::= "solutionModule" [function, total]

  // Exact mathematical summaries of the three source loops.
  syntax Float ::= polyAcc(NumSeq, Float, Float, Float)
                   [function, total, symbol(polyAcc), no-evaluators]
                 | polyValue(NumSeq, Float)
                   [function, total, symbol(polyValue), no-evaluators]
                 | polyPower(NumSeq, Float, Float)
                   [function, total, symbol(polyPower), no-evaluators]
                 | bracketBegin(NumSeq, Float, Float)
                   [function, total, symbol(bracketBegin), no-evaluators]
                 | bracketEnd(NumSeq, Float, Float)
                   [function, total, symbol(bracketEnd), no-evaluators]
                 | solveFrom(NumSeq, Float, Float)
                   [function, total, symbol(solveFrom), no-evaluators]
                 | bisectFrom(NumSeq, Float, Float)
                   [function, total, symbol(bisectFrom), no-evaluators]
  syntax Val ::= polyLast(NumSeq, Val)
                 [function, total, symbol(polyLast), no-evaluators]
endmodule

module VERIFICATION-BASE
  imports MPY
  imports VERIFICATION-SYNTAX

  rule numVals(.NumSeq) => .ValSeq
  rule numVals(nInt(I, NS)) => vCons(I, numVals(NS))
  rule numVals(nFloat(F, NS)) => vCons(F, numVals(NS))

  // Injectivity consequences of the three disjoint embedding equations.
  // These expose the NumSeq constructor selected by MPY's ValSeq iterator.
  rule { numVals(@NS:NumSeq) #Equals .ValSeq }
    => { @NS #Equals .NumSeq }
    [simplification]
  rule { numVals(@NS1:NumSeq) #Equals numVals(@NS2:NumSeq) }
    => { @NS1 #Equals @NS2 }
    [simplification]
  rule { numVals(@NS:NumSeq)
         #Equals vCons(@I:Int, numVals(@R:NumSeq)) }
    => { @NS #Equals nInt(@I, @R) }
    [simplification]
  rule { numVals(@NS:NumSeq)
         #Equals vCons(@F:Float, numVals(@R:NumSeq)) }
    => { @NS #Equals nFloat(@F, @R) }
    [simplification]

  rule numLen(.NumSeq) => 0
  rule numLen(nInt(_, NS)) => 1 +Int numLen(NS)
  rule numLen(nFloat(_, NS)) => 1 +Int numLen(NS)

  rule lastNonZero(.NumSeq) => false
  rule lastNonZero(nInt(I, .NumSeq)) => I =/=Int 0
  rule lastNonZero(nFloat(F, .NumSeq)) => notBool eqF(F, 0.0)
  rule lastNonZero(nInt(_, NS)) => lastNonZero(NS)
    requires numLen(NS) >Int 0
  rule lastNonZero(nFloat(_, NS)) => lastNonZero(NS)
    requires numLen(NS) >Int 0

  rule validCoeffs(NS)
    => numLen(NS) >=Int 2
       andBool numLen(NS) %Int 2 ==Int 0
       andBool lastNonZero(NS)

  rule polyStep
    => Assign(
         Name("value"),
         BinOp("+", Name("value"),
                    BinOp("*", Name("coeff"), Name("power"))))
       Assign(Name("power"), BinOp("*", Name("power"), Name("x")))

  rule polyBody
    => Assign(Name("value"), Float(0.0))
       Assign(Name("power"), Float(1.0))
       Assign(Name("coeff"), Float(0.0))
       For(Name("coeff"), Name("xs"), polyStep)
       Return(Name("value"))

  rule expandCond
    => Compare(
         BinOp("*",
           Call(Name("poly"), (Name("xs"), Name("begin"), .Exprs)),
           Call(Name("poly"), (Name("xs"), Name("end"), .Exprs))),
         CmpOp(">", Float(0.0)))

  rule expandBody
    => Assign(Name("begin"), BinOp("*", Name("begin"), Float(2.0)))
       Assign(Name("end"), BinOp("*", Name("end"), Float(2.0)))

  rule bisectCond
    => Compare(
         BinOp("-", Name("end"), Name("begin")),
         CmpOp(">", Float(1e-10)))

  rule bisectBody
    => Assign(
         Name("center"),
         BinOp("/", BinOp("+", Name("begin"), Name("end")), Float(2.0)))
       If(
         Compare(
           BinOp("*",
             Call(Name("poly"), (Name("xs"), Name("center"), .Exprs)),
             Call(Name("poly"), (Name("xs"), Name("begin"), .Exprs))),
           CmpOp(">", Float(0.0))),
         Assign(Name("begin"), Name("center")),
         Assign(Name("end"), Name("center")))

  rule findZeroBody
    => Assign(
         Name("begin"),
         BinOp("/",
           Call(Name("len"), (Name("xs"), .Exprs)),
           UnaryOp("-", Call(Name("len"), (Name("xs"), .Exprs)))))
       Assign(
         Name("end"),
         BinOp("/",
           Call(Name("len"), (Name("xs"), .Exprs)),
           Call(Name("len"), (Name("xs"), .Exprs))))
       Assign(Name("center"), Float(0.0))
       While(expandCond, expandBody)
       While(bisectCond, bisectBody)
       Return(Name("begin"))

  rule solutionModule
    => Module(
         FuncDef("poly", Params(("xs", "x")), polyBody)
         FuncDef("find_zero", Params("xs"), findZeroBody))

  // Horner-by-powers fold used by poly.  Both clauses are exact restatements
  // of one source iteration for the corresponding numeric constructor.
  rule polyAcc(.NumSeq, _X, A, _P) => A [simplification]
  rule polyAcc(nInt(I, NS), X, A, P)
    => polyAcc(NS, X,
               addF(A, mulF(intToF(I), P)),
               mulF(P, X))
    [simplification]
  rule polyAcc(nFloat(F, NS), X, A, P)
    => polyAcc(NS, X,
               addF(A, mulF(F, P)),
               mulF(P, X))
    [simplification]
  rule polyValue(NS, X) => polyAcc(NS, X, 0.0, 1.0)
    [simplification]
  rule polyPower(.NumSeq, _X, P) => P [simplification]
  rule polyPower(nInt(_I, NS), X, P)
    => polyPower(NS, X, mulF(P, X))
    [simplification]
  rule polyPower(nFloat(_F, NS), X, P)
    => polyPower(NS, X, mulF(P, X))
    [simplification]
  rule polyLast(.NumSeq, C) => C [simplification]
  rule polyLast(nInt(I, NS), _C)
    => polyLast(NS, I)
    [simplification]
  rule polyLast(nFloat(F, NS), _C)
    => polyLast(NS, F)
    [simplification]

  // Exact projections of the pair of endpoints produced by the expansion
  // loop.  Their guards are the source guard and its negation.
  rule bracketBegin(NS, B, E)
    => bracketBegin(NS, mulF(B, 2.0), mulF(E, 2.0))
    requires gtF(mulF(polyValue(NS, B), polyValue(NS, E)), 0.0)
    [simplification]
  rule bracketBegin(NS, B, E) => B
    requires notBool gtF(mulF(polyValue(NS, B), polyValue(NS, E)), 0.0)
    [simplification]
  rule bracketEnd(NS, B, E)
    => bracketEnd(NS, mulF(B, 2.0), mulF(E, 2.0))
    requires gtF(mulF(polyValue(NS, B), polyValue(NS, E)), 0.0)
    [simplification]
  rule bracketEnd(NS, B, E) => E
    requires notBool gtF(mulF(polyValue(NS, B), polyValue(NS, E)), 0.0)
    [simplification]

  // The bisection loop summary.  The outer clauses split on the while guard;
  // the two recursive clauses then split on the exact source if-condition.
  rule bisectFrom(NS, B, E)
    => bisectFrom(NS, divF(addF(B, E), 2.0), E)
    requires gtF(subF(E, B), 1e-10)
      andBool gtF(
        mulF(polyValue(NS, divF(addF(B, E), 2.0)),
             polyValue(NS, B)),
        0.0)
    [simplification]
  rule bisectFrom(NS, B, E)
    => bisectFrom(NS, B, divF(addF(B, E), 2.0))
    requires gtF(subF(E, B), 1e-10)
      andBool notBool gtF(
        mulF(polyValue(NS, divF(addF(B, E), 2.0)),
             polyValue(NS, B)),
        0.0)
    [simplification]
  rule bisectFrom(_NS, B, E)
    => B
    requires notBool gtF(subF(E, B), 1e-10)
    [simplification]

  rule solveFrom(NS, B, E)
    => bisectFrom(NS, bracketBegin(NS, B, E), bracketEnd(NS, B, E))
    [simplification]
endmodule

module VERIFICATION
  imports VERIFICATION-BASE
endmodule
