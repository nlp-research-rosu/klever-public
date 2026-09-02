requires "reference-semantics/semantics.k"

module PROD-SIGNS-VERIFICATION
  imports MPY

  // These two left folds state the two factors in the task's contract.
  // Their equations deliberately mirror addition of |I| and multiplication
  // by sign(I), respectively.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(_I:Int, VS:ValSeq)) => allInts(VS)
  rule allInts(vCons(_V:Val, _VS:ValSeq)) => false [owise]

  syntax Int ::= magnitudeAcc(ValSeq, Int) [function, total]
  rule magnitudeAcc(.ValSeq, A:Int) => A
  rule magnitudeAcc(vCons(I:Int, VS:ValSeq), A:Int)
    => magnitudeAcc(VS, A -Int I)
    requires I <Int 0
  rule magnitudeAcc(vCons(I:Int, VS:ValSeq), A:Int)
    => magnitudeAcc(VS, A +Int I)
    requires I >=Int 0

  syntax Int ::= signAcc(ValSeq, Int) [function, total]
  rule signAcc(.ValSeq, S:Int) => S
  rule signAcc(vCons(I:Int, VS:ValSeq), S:Int)
    => signAcc(VS, 0 -Int S)
    requires I <Int 0
  rule signAcc(vCons(0, VS:ValSeq), _S:Int)
    => signAcc(VS, 0)
  rule signAcc(vCons(I:Int, VS:ValSeq), S:Int)
    => signAcc(VS, S)
    requires I >Int 0

  syntax Int ::= magnitudeSum(ValSeq) [function, total]
               | signProduct(ValSeq)  [function, total]
               | lastInt(ValSeq)      [function, total]
  rule magnitudeSum(VS:ValSeq) => magnitudeAcc(VS, 0)
  rule signProduct(VS:ValSeq) => signAcc(VS, 1)
  rule lastInt(vCons(I:Int, .ValSeq)) => I
  rule lastInt(vCons(_I:Int, vCons(J:Int, VS:ValSeq)))
    => lastInt(vCons(J, VS))

  // The exact closure translated from solution.py. The string expression is
  // the function docstring; MPY evaluates it as a discarded expression.
  syntax Val ::= "prodSignsFunction" [macro]
  rule prodSignsFunction
    => closureVal(
         "arr",
         Expr(Str(
           "\n    Return the sum of the magnitudes in arr multiplied by the product of\n    their signs.  The empty input has no such product and returns None.\n    "))
         If(Compare(Name("arr"), CmpOp("==", ListExpr(.Exprs))),
           Return(NoneVal),
           .Stmts)
         Assign(Name("total"), Int(0))
         Assign(Name("sign"), Int(1))
         For(Name("value"), Name("arr"),
           If(Compare(Name("value"), CmpOp("<", Int(0))),
             Assign(Name("total"),
               BinOp("-", Name("total"), Name("value")))
             Assign(Name("sign"),
               BinOp("-", Int(0), Name("sign"))),
             Assign(Name("total"),
               BinOp("+", Name("total"), Name("value")))
             If(Compare(Name("value"), CmpOp("==", Int(0))),
               Assign(Name("sign"), Int(0)),
               .Stmts)))
         Return(BinOp("*", Name("total"), Name("sign"))),
         0)

  // Loop-summary invariant for the exact loop above. It is applicable only to
  // integer lists (the precondition is carried by the claims). It updates
  // the two accumulators and the loop variable exactly as ordinary execution
  // does, so later code observes the same local state.
  rule <k>
         For(Name("value"), list(vCons(I:Int, VS:ValSeq)),
           If(Compare(Name("value"), CmpOp("<", Int(0))),
             Assign(Name("total"),
               BinOp("-", Name("total"), Name("value")))
             Assign(Name("sign"),
               BinOp("-", Int(0), Name("sign"))),
             Assign(Name("total"),
               BinOp("+", Name("total"), Name("value")))
             If(Compare(Name("value"), CmpOp("==", Int(0))),
               Assign(Name("sign"), Int(0)),
               .Stmts)))
         =>
         .K
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           M:Map
             => M
                  [ "total" <- magnitudeAcc(
                      vCons(I, VS), {M["total"]}:>Int) ]
                  [ "sign" <- signAcc(
                      vCons(I, VS), {M["sign"]}:>Int) ]
                  [ "value" <- lastInt(vCons(I, VS)) ],
           P:Parent)
         ...
       </scopes>
       requires "total" in_keys(M) andBool "sign" in_keys(M)
        andBool allInts(VS)
       [priority(40)]
endmodule
