requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports MPY-CORE
  imports FLOAT

  syntax Bool ::= allFloatVS(ValSeq) [function, total]
  syntax Float ::= projectFloat(Val)
      [function, total, symbol(projectFloat), no-evaluators]
  syntax Float ::= sumFloatVS(ValSeq, Float) [function, total]
  syntax Float ::= deviationFloatVS(ValSeq, Float, Float)
      [function, total]
  syntax Float ::= madResult(ValSeq) [function, total]

  syntax Stmts ::= "madBody" [macro]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY
  imports BOOL
  imports K-EQUAL

  // The exact translated body of solution.py.
  rule madBody
    => Assign(Name("count"), Call(Name("len"), Name("numbers")))
       If(Compare(Name("count"), CmpOp("==", Int(0))),
          Return(Float(0.0)),
          .Stmts)
       Assign(Name("total"), Float(0.0))
       Assign(Name("number"), Float(0.0))
       For(Name("number"), Name("numbers"),
           Assign(Name("total"),
                  BinOp("+", Name("total"), Name("number"))))
       Assign(Name("mean"), BinOp("/", Name("total"), Name("count")))
       Assign(Name("deviation"), Float(0.0))
       For(Name("number"), Name("numbers"),
           Assign(Name("deviation"),
                  BinOp("+",
                        Name("deviation"),
                        Call(Name("abs"),
                             BinOp("-", Name("number"), Name("mean"))))))
       Return(BinOp("/", Name("deviation"), Name("count")))

  // A recursive domain predicate for arbitrary finite lists of floats.
  rule allFloatVS(.ValSeq) => true
  rule allFloatVS(vCons(V:Val, R:ValSeq))
    => isFloat(V) andBool allFloatVS(R)

  // Total only to give the backend a static Float term.  On the theorem
  // domain every use is guarded by allFloatVS/isFloat, and the collapse rule
  // makes it the identity for an actual Float.
  rule #Ceil({@V:Val}:>Float)
    => ({ isFloat(@V) #Equals true } #And #Ceil(@V))
    [simplification]
  rule projectFloat(V:Val) => {V}:>Float
    requires isFloat(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Float => projectFloat(V)
    requires isFloat(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectFloat(F:Float) => F [simplification]

  // Guarded dispatch twins of MPY-FLOAT's typed rules.  They do not replace
  // a computation; they restate the same equations after the domain guard.
  rule applyBin("+", A:Float, V:Val)
    => addF(A, projectFloat(V))
    requires isFloat(V)
    [simplification]
  rule applyBin("-", V:Val, M:Float)
    => subF(projectFloat(V), M)
    requires isFloat(V)
    [simplification]

  // Exact left folds used by the two loop circularities.
  rule sumFloatVS(.ValSeq, A:Float) => A
  rule sumFloatVS(vCons(V:Val, R:ValSeq), A:Float)
    => sumFloatVS(R, addF(A, projectFloat(V)))

  rule deviationFloatVS(.ValSeq, _:Float, A:Float) => A
  rule deviationFloatVS(vCons(V:Val, R:ValSeq), M:Float, A:Float)
    => deviationFloatVS(
         R,
         M,
         addF(A, absF(subF(projectFloat(V), M))))

  rule madResult(VS:ValSeq) => 0.0
    requires vsLen(VS) ==Int 0
  rule madResult(VS:ValSeq)
    => divFloatIntV(
         deviationFloatVS(
           VS,
           divFloatIntV(
             sumFloatVS(VS, 0.0),
             vsLen(VS)),
           0.0),
         vsLen(VS))
    requires vsLen(VS) =/=Int 0
endmodule
