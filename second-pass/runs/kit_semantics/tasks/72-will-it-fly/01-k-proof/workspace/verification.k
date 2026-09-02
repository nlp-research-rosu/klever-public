requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-CORE
  imports BOOL
  imports INT

  syntax Bool ::= allIntegral(ValSeq)
    [function, total, symbol(allIntegral), no-evaluators]
  syntax Bool ::= allNumeric(ValSeq)
    [function, total, symbol(allNumeric), no-evaluators]
  syntax Bool ::= hasFloat(ValSeq)
    [function, total, symbol(hasFloat), no-evaluators]
  syntax Bool ::= integralV(Val) [function, total]
  syntax Bool ::= floatV(Val) [function, total]
  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]
  syntax Bool ::= projectBoolTotal(Val)
    [function, total, symbol(projectBoolTotal), no-evaluators]
  syntax Float ::= projectFloatTotal(Val)
    [function, total, symbol(projectFloatTotal), no-evaluators]
  syntax Int ::= intLikeTotal(Val)
    [function, total, symbol(intLikeTotal), no-evaluators]
  syntax Int ::= sumInts(Int, ValSeq)
    [function, total, symbol(sumInts), no-evaluators]
  syntax Float ::= sumFloatRest(Float, ValSeq)
    [function, total, symbol(sumFloatRest), no-evaluators]
  syntax Float ::= sumToFloat(Int, ValSeq)
    [function, total, symbol(sumToFloat), no-evaluators]
  syntax Float ::= noFloatSum(Int)
    [function, total, symbol(noFloatSum), no-evaluators]
  syntax ValSeq ::= reverseSlice(ValSeq)
    [function, total, symbol(reverseSlice), no-evaluators]
  syntax Val ::= willItFlyClosure() [function, total]
endmodule

module VERIFICATION-BASE
  imports MPY
  imports VERIFICATION-SYNTAX

  // Mutually exclusive classifiers for the disjoint K Val alternatives.
  rule integralV(V:Val)
    => ( (isInt(V) andBool notBool isBool(V))
         orBool
         (isBool(V) andBool notBool isInt(V)) )
       andBool notBool isFloat(V)
  rule floatV(V:Val)
    => isFloat(V)
       andBool notBool isInt(V)
       andBool notBool isBool(V)

  // Ground equations fix the summaries' interpretation in the target theory
  // without forcing unbounded symbolic evaluator unfolding.
  rule allIntegral(.ValSeq) => true [concrete, simplification]
  rule allIntegral(vCons(V:Val, R:ValSeq))
    => integralV(V) andBool allIntegral(R)
    [concrete, simplification]

  rule sumInts(ACC:Int, .ValSeq) => ACC [concrete, simplification]
  rule sumInts(ACC:Int, vCons(V:Val, R:ValSeq))
    => sumInts(ACC +Int intLikeTotal(V), R)
    [concrete, simplification]

  rule allNumeric(.ValSeq) => true [concrete, simplification]
  rule allNumeric(vCons(V:Val, R:ValSeq))
    => (integralV(V) orBool floatV(V))
       andBool allNumeric(R)
    [concrete, simplification]

  rule hasFloat(.ValSeq) => false [concrete, simplification]
  rule hasFloat(vCons(V:Val, R:ValSeq))
    => floatV(V) orBool hasFloat(R)
    [concrete, simplification]

  rule sumFloatRest(ACC:Float, .ValSeq) => ACC
    [concrete, simplification]
  rule sumFloatRest(ACC:Float, vCons(V:Val, R:ValSeq))
    => sumFloatRest(addF(ACC, projectFloatTotal(V)), R)
    requires floatV(V)
    [concrete, simplification]
  rule sumFloatRest(ACC:Float, vCons(V:Val, R:ValSeq))
    => sumFloatRest(addF(ACC, intToF(intLikeTotal(V))), R)
    requires integralV(V)
    [concrete, simplification]
  rule sumFloatRest(ACC:Float, vCons(V:Val, R:ValSeq))
    => sumFloatRest(ACC, R)
    requires
      notBool (floatV(V) orBool integralV(V))
    [concrete, simplification]

  rule sumToFloat(ACC:Int, .ValSeq) => noFloatSum(ACC)
    [concrete, simplification]
  rule sumToFloat(ACC:Int, vCons(V:Val, R:ValSeq))
    => sumFloatRest(addF(intToF(ACC), projectFloatTotal(V)), R)
    requires floatV(V)
    [concrete, simplification]
  rule sumToFloat(ACC:Int, vCons(V:Val, R:ValSeq))
    => sumToFloat(ACC +Int intLikeTotal(V), R)
    requires integralV(V)
    [concrete, simplification]
  rule sumToFloat(ACC:Int, vCons(V:Val, R:ValSeq))
    => sumToFloat(ACC, R)
    requires
      notBool (floatV(V) orBool integralV(V))
    [concrete, simplification]

  rule reverseSlice(VS:ValSeq)
    => buildVS(VS, vsLen(VS) +Int -1, -1, -1)
    [concrete]

  // A guarded total projection supplies the static Int view justified by
  // allIntegral; they cannot manufacture a projected value outside its guard.
  rule projectIntTotal(I:Int) => I [simplification]
  rule projectIntTotal(V:Val) => {V}:>Int
    requires
      isInt(V) andBool notBool isBool(V) andBool notBool isFloat(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Int => projectIntTotal(V)
    requires
      isInt(V) andBool notBool isBool(V) andBool notBool isFloat(V)
    [symbolic(V), simplification, preserves-definedness]
  rule #Ceil({V:Val}:>Int)
    => ({ isInt(V) #Equals true } #And #Ceil(V))
    [simplification]

  rule projectBoolTotal(B:Bool) => B [simplification]
  rule projectBoolTotal(V:Val) => {V}:>Bool
    requires
      isBool(V) andBool notBool isInt(V) andBool notBool isFloat(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Bool => projectBoolTotal(V)
    requires
      isBool(V) andBool notBool isInt(V) andBool notBool isFloat(V)
    [symbolic(V), simplification, preserves-definedness]
  rule #Ceil({V:Val}:>Bool)
    => ({ isBool(V) #Equals true } #And #Ceil(V))
    [simplification]

  rule projectFloatTotal(F:Float) => F [simplification]
  rule projectFloatTotal(V:Val) => {V}:>Float
    requires floatV(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Float => projectFloatTotal(V)
    requires floatV(V)
    [symbolic(V), simplification, preserves-definedness]
  rule #Ceil({V:Val}:>Float)
    => ({ isFloat(V) #Equals true } #And #Ceil(V))
    [simplification]

  rule intLikeTotal(V:Val) => projectIntTotal(V)
    requires
      isInt(V) andBool notBool isBool(V) andBool notBool isFloat(V)
    [simplification]
  rule intLikeTotal(V:Val)
    => #if projectBoolTotal(V) #then 1 #else 0 #fi
    requires
      isBool(V) andBool notBool isInt(V) andBool notBool isFloat(V)
    [simplification]

  // Guarded dispatch twin of the two fixed intOf rules.
  rule intOf(V:Val) => intLikeTotal(V)
    requires integralV(V)
    [simplification]

  // Exact translated body of solution.py, named only to keep the two target
  // claims textually identical. It is still executed by MPY-FUNCTIONS.
  rule willItFlyClosure()
    => closureVal(
         ("q", "w", .ParamNames),
         Return(
           BoolOp(
             "and",
             ( Compare(
                 Name("q"),
                 CmpOp(
                   "==",
                   Subscript(
                     Name("q"),
                     Slice(
                       NoBound,
                       NoBound,
                       UnaryOp("-", Int(1))))))
             , Compare(
                 Call(Name("sum"), (Name("q"), .Exprs)),
                 CmpOp("<=", Name("w")))
             , .Exprs)))
           .Stmts,
         0)
endmodule

module SUMMARY-DEFINITION
  imports VERIFICATION-BASE

  // Exhaustive definitions used only by the bridge-free connection build.
  rule allIntegral(.ValSeq) => true
  rule allIntegral(vCons(V:Val, R:ValSeq))
    => integralV(V) andBool allIntegral(R)

  rule sumInts(ACC:Int, .ValSeq) => ACC
  rule sumInts(ACC:Int, vCons(V:Val, R:ValSeq))
    => sumInts(ACC +Int intLikeTotal(V), R)

  rule allNumeric(.ValSeq) => true
  rule allNumeric(vCons(V:Val, R:ValSeq))
    => (integralV(V) orBool floatV(V))
       andBool allNumeric(R)

  rule hasFloat(.ValSeq) => false
  rule hasFloat(vCons(V:Val, R:ValSeq))
    => floatV(V) orBool hasFloat(R)

  rule sumFloatRest(ACC:Float, .ValSeq) => ACC
    [simplification]
  rule sumFloatRest(ACC:Float, vCons(V:Val, R:ValSeq))
    => sumFloatRest(addF(ACC, projectFloatTotal(V)), R)
    requires floatV(V)
    [simplification]
  rule sumFloatRest(ACC:Float, vCons(V:Val, R:ValSeq))
    => sumFloatRest(addF(ACC, intToF(intLikeTotal(V))), R)
    requires integralV(V)
    [simplification]
  rule sumFloatRest(ACC:Float, vCons(V:Val, R:ValSeq))
    => sumFloatRest(ACC, R)
    requires
      notBool (floatV(V) orBool integralV(V))
    [simplification]

  rule sumToFloat(ACC:Int, .ValSeq) => noFloatSum(ACC)
    [simplification]
  rule sumToFloat(ACC:Int, vCons(V:Val, R:ValSeq))
    => sumFloatRest(addF(intToF(ACC), projectFloatTotal(V)), R)
    requires floatV(V)
    [simplification]
  rule sumToFloat(ACC:Int, vCons(V:Val, R:ValSeq))
    => sumToFloat(ACC +Int intLikeTotal(V), R)
    requires integralV(V)
    [simplification]
  rule sumToFloat(ACC:Int, vCons(V:Val, R:ValSeq))
    => sumToFloat(ACC, R)
    requires
      notBool (floatV(V) orBool integralV(V))
    [simplification]

  rule reverseSlice(VS:ValSeq)
    => buildVS(VS, vsLen(VS) +Int -1, -1, -1)
    [simplification]
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Exact slice continuation bridge; allocation remains a fixed-semantics
  // step. SUM-CONNECTION.reverse-slice proves this complete context.
  rule <k> someB(-1) ~> #slStep(list(VS:ValSeq), noB, noB)
        => #alloc(list(reverseSlice(VS))) ... </k>
    [priority(40)]

  // Operational bridge whose complete match domain is proved, without this
  // rule, by SUM-CONNECTION.sum-fold under SUMMARY-DEFINITION.
  rule <k> #iterNext(list(VS:ValSeq)) ~> #sumCont(ACC:Int)
        => sumInts(ACC, VS) ... </k>
    requires allIntegral(VS) andBool notBool hasFloat(VS)
    [priority(40)]

  // Float-containing fold bridge, proved in FLOAT-SUM-CONNECTION after the
  // independently connected float-rest bridge is installed.
  rule <k> #iterNext(list(VS:ValSeq)) ~> #sumCont(ACC:Int)
        => sumToFloat(ACC, VS) ... </k>
    requires
      allNumeric(VS)
      andBool hasFloat(VS)
      andBool notBool allIntegral(VS)
    [priority(39)]
endmodule

module FLOAT-REST-VERIFICATION
  imports SUMMARY-DEFINITION

  rule <k> #iterNext(list(VS:ValSeq)) ~> #sumContF(ACC:Float)
        => sumFloatRest(ACC, VS) ... </k>
    requires allNumeric(VS)
    [priority(40)]
endmodule
