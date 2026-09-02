requires "reference-semantics/semantics.k"

module COUNT-NUMS-VERIFICATION-BASE
  imports MPY

  // Mathematical model of base-10 digit processing for nonnegative inputs.
  syntax Int ::= digitQuot(Int) [function, total]
  rule digitQuot(N:Int) => (N -Int pyMod(N, 10)) /Int 10

  syntax Int ::= positiveFold(Int, Int) [function, total]
  rule positiveFold(N:Int, A:Int) => A requires N <=Int 0
  rule positiveFold(N:Int, A:Int)
    => positiveFold(digitQuot(N), A +Int pyMod(N, 10))
    requires N >Int 0

  syntax Int ::= positiveDigitSum(Int) [function, total]
  rule positiveDigitSum(N:Int) => positiveFold(N, 0)

  // For a negative original input, the magnitude's leading digit is negated.
  syntax Int ::= leadingDigit(Int) [function, total]
  rule leadingDigit(N:Int) => N
    requires N <Int 10
  rule leadingDigit(N:Int) => leadingDigit(digitQuot(N))
    requires N >=Int 10

  syntax Int ::= negativeTotal(Int, Int) [function, total]
  rule negativeTotal(N:Int, A:Int) => A
    requires N <Int 10
  rule negativeTotal(N:Int, A:Int)
    => negativeTotal(digitQuot(N), A +Int pyMod(N, 10))
    requires N >=Int 10

  syntax Int ::= negativeDigitSum(Int) [function, total]
  rule negativeDigitSum(N:Int)
    => negativeTotal(N, 0) -Int leadingDigit(N)

  syntax Int ::= signedDigitSum(Int) [function, total]
  rule signedDigitSum(N:Int) => negativeDigitSum(0 -Int N)
    requires N <Int 0
  rule signedDigitSum(N:Int) => positiveDigitSum(N)
    requires N >=Int 0

  // Total proof-level projection used only under an isInt(V) path condition.
  syntax Int ::= intValue(Val) [function, total]
  rule intValue(N:Int) => N
  rule intValue(_:Val) => 0 [owise]

  syntax Int ::= positiveBit(Int) [function, total]
  rule positiveBit(N:Int) => 1 requires N >Int 0
  rule positiveBit(N:Int) => 0 requires N <=Int 0

  syntax Int ::= countFold(ValSeq, Int) [function, total]
  rule countFold(.ValSeq, C:Int) => C
  rule countFold(vCons(V:Val, REST:ValSeq), C:Int)
    => countFold(REST,
                 C +Int positiveBit(signedDigitSum(intValue(V))))
    requires isInt(V)

  syntax Int ::= countPositive(ValSeq) [function, total]
  rule countPositive(VS:ValSeq) => countFold(VS, 0)

  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq))
    => isInt(V) andBool allInts(REST)

  // The loop target remains bound after a Python for-loop.
  syntax Val ::= lastOr(ValSeq, Val) [function, total]
  rule lastOr(.ValSeq, OLD:Val) => OLD
  rule lastOr(vCons(V:Val, REST:ValSeq), _OLD:Val)
    => lastOr(REST, V)

  // Exact statement blocks emitted in solution.mpy.
  syntax Stmts ::= "positiveLoopBody" [macro]
  rule positiveLoopBody
    => AugAssign(Name("total"), "+", BinOp("%", Name("n"), Int(10)))
       AugAssign(Name("n"), "//", Int(10))

  syntax Stmts ::= "negativeLoopBody" [macro]
  rule negativeLoopBody
    => AugAssign(Name("total"), "+", BinOp("%", Name("n"), Int(10)))
       AugAssign(Name("n"), "//", Int(10))

  syntax Stmts ::= "positiveFunctionBody" [macro]
  rule positiveFunctionBody
    => Assign(Name("total"), Int(0))
       While(Compare(Name("n"), CmpOp(">", Int(0))), positiveLoopBody)
       Return(Name("total"))

  syntax Stmts ::= "negativeFunctionBody" [macro]
  rule negativeFunctionBody
    => Assign(Name("total"), Int(0))
       While(Compare(Name("n"), CmpOp(">=", Int(10))), negativeLoopBody)
       Return(BinOp("-", Name("total"), Name("n")))

  syntax Stmts ::= "signedFunctionBody" [macro]
  rule signedFunctionBody
    => If(Compare(Name("n"), CmpOp("<", Int(0))),
          Return(Call(Name("negative_digit_sum"),
                      BinOp("-", Int(0), Name("n")))),
          .Stmts)
       Return(Call(Name("positive_digit_sum"), Name("n")))

  syntax Stmts ::= "countLoopBody" [macro]
  rule countLoopBody
    => If(Compare(Call(Name("signed_digit_sum"), Name("n")),
                 CmpOp(">", Int(0))),
          AugAssign(Name("count"), "+", Int(1)),
          .Stmts)

  syntax Stmts ::= "countFunctionBody" [macro]
  rule countFunctionBody
    => Assign(Name("count"), Int(0))
       For(Name("n"), Name("arr"), countLoopBody)
       Return(Name("count"))

  syntax Val ::= "positiveDigitClosure" [macro]
  rule positiveDigitClosure
    => closureVal("n", positiveFunctionBody, 0)

  syntax Val ::= "negativeDigitClosure" [macro]
  rule negativeDigitClosure
    => closureVal("n", negativeFunctionBody, 0)

  syntax Val ::= "signedDigitClosure" [macro]
  rule signedDigitClosure
    => closureVal("n", signedFunctionBody, 0)

  syntax Val ::= "countNumsClosure" [macro]
  rule countNumsClosure
    => closureVal("arr", countFunctionBody, 0)

  syntax Map ::= "digitFunctionBindings" [macro]
  rule digitFunctionBindings
    => ("positive_digit_sum" |-> positiveDigitClosure
        "negative_digit_sum" |-> negativeDigitClosure
        "signed_digit_sum"   |-> signedDigitClosure)
endmodule

// These rules are the already-proved loop invariants, exposed as reusable
// semantic lemmas for the function-level claims.
module DIGIT-LOOP-LEMMAS
  imports COUNT-NUMS-VERIFICATION-BASE

  rule <k> #while(Compare(Name("n"), CmpOp(">", Int(0))),
                   positiveLoopBody) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("n" |-> N:Int "total" |-> A:Int)
           => ("n" |-> 0
               "total" |-> positiveFold(N, A)),
           P:Parent)
         ...
       </scopes>
       requires N >=Int 0
       [priority(40)]

  rule <k> #while(Compare(Name("n"), CmpOp(">=", Int(10))),
                   negativeLoopBody) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("n" |-> N:Int "total" |-> A:Int)
           => ("n" |-> leadingDigit(N)
               "total" |-> negativeTotal(N, A)),
           P:Parent)
         ...
       </scopes>
       requires N >=Int 0
       [priority(40)]
endmodule

module DIGIT-FUNCTION-LEMMAS
  imports DIGIT-LOOP-LEMMAS

  rule <k> #applyK(toCall(positiveDigitClosure), (N:Int, .Vals))
        => positiveDigitSum(N) ... </k>
       requires N >=Int 0
       [priority(40)]

  rule <k> #applyK(toCall(negativeDigitClosure), (N:Int, .Vals))
        => negativeDigitSum(N) ... </k>
       requires N >=Int 0
       [priority(40)]
endmodule

module SIGNED-DIGIT-LEMMA
  imports DIGIT-FUNCTION-LEMMAS

  rule <k> #applyK(toCall(signedDigitClosure), (V:Val, .Vals))
        => signedDigitSum(intValue(V)) ... </k>
       requires isInt(V)
       [priority(40)]
endmodule

module COUNT-LOOP-WITH-N-LEMMA
  imports SIGNED-DIGIT-LEMMA

  rule <k> #loop(list(VS:ValSeq), Name("n"), countLoopBody) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("arr" |-> list(ALL:ValSeq)
               "count" |-> C:Int
            "n" |-> OLD:Val)
           => ("arr" |-> list(ALL)
               "count" |-> countFold(VS, C)
               "n" |-> lastOr(VS, OLD)),
           parent(0))
         ...
       </scopes>
       requires allInts(VS)
       [priority(40)]
endmodule

module COUNT-LOOP-LEMMA
  imports COUNT-LOOP-WITH-N-LEMMA

  rule <k> #loop(list(.ValSeq), Name("n"), countLoopBody) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("arr" |-> list(ALL:ValSeq) "count" |-> C:Int),
           parent(0))
         ...
       </scopes>
       [priority(40)]

  rule <k> #loop(list(vCons(H:Val, REST:ValSeq)),
                  Name("n"), countLoopBody) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("arr" |-> list(ALL:ValSeq) "count" |-> C:Int)
           => ("arr" |-> list(ALL)
               "count" |-> countFold(vCons(H, REST), C)
               "n" |-> lastOr(REST, H)),
           parent(0))
         ...
       </scopes>
       requires isInt(H) andBool allInts(REST)
       [priority(40)]
endmodule

module COUNT-NUMS-VERIFICATION
  imports COUNT-LOOP-LEMMA
endmodule
