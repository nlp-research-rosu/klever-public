requires "reference-semantics/semantics.k"

module UNIQUE-DIGITS-SPEC-SYNTAX
  imports MPY

  // Symbolic abstraction of the concrete digit-scanning helper.  Like the
  // reference semantics' sortVS, this stays opaque on symbolic arguments;
  // concrete LLVM runs exercise the actual Python helper.
  syntax Bool ::= oddDigits(Int)
    [function, total, symbol(oddDigits), no-evaluators]

  // Append precisely the all-odd-digit members of the remaining input to ACC.
  // This accumulator form is the invariant of the source-level for loop.
  syntax ValSeq ::= filterOddAcc(ValSeq, ValSeq) [function]
  rule filterOddAcc(ACC:ValSeq, .ValSeq) => ACC
  rule filterOddAcc(ACC:ValSeq, vCons(N:Int, REST:ValSeq))
    => filterOddAcc(
         valSeqConcat(ACC, vCons(N, .ValSeq)),
         REST)
    requires oddDigits(N) ==K true
  rule filterOddAcc(ACC:ValSeq, vCons(N:Int, REST:ValSeq))
    => filterOddAcc(ACC, REST)
    requires oddDigits(N) ==K false

  syntax Val ::= lastInput(Val, ValSeq) [function, total]
  rule lastInput(OLD:Val, .ValSeq) => OLD
  rule lastInput(_:Val, vCons(V:Val, REST:ValSeq))
    => lastInput(V, REST)

  syntax Bool ::= positiveInts(ValSeq) [function, total]
  rule positiveInts(.ValSeq) => true
  rule positiveInts(vCons(N:Int, REST:ValSeq))
    => N >Int 0 andBool positiveInts(REST)
  rule positiveInts(vCons(V:Val, _:ValSeq)) => false
    requires notBool isInt(V)

  syntax Stmts ::= "digitLoopBody" [macro]
  rule digitLoopBody
    => If(Compare(BinOp("%", Name("n"), Int(2)),
                  CmpOp("==", Int(0))),
          Assign(Name("result"), Bool(false))
          Break,
          .Stmts)
       AugAssign(Name("n"), "//", Int(10))

  syntax Stmts ::= "oddDigitsBody" [macro]
  rule oddDigitsBody
    => Assign(Name("result"), Bool(true))
       While(Compare(Name("n"), CmpOp(">", Int(0))),
             digitLoopBody)
       Return(Name("result"))

  syntax Stmts ::= "filterLoopBody" [macro]
  rule filterLoopBody
    => If(Call(Name("_all_digits_odd"), Name("n")),
          Expr(Call(Attribute(Name("result"), "append"), Name("n"))),
          .Stmts)

  syntax Stmts ::= "uniqueDigitsBody" [macro]
  rule uniqueDigitsBody
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("n"), Int(0))
       For(Name("n"), Name("x"), filterLoopBody)
       Return(Call(Name("sorted"), Name("result")))
endmodule

// Base symbolic vocabulary.
module UNIQUE-DIGITS-BASE
  imports UNIQUE-DIGITS-SPEC-SYNTAX
endmodule

// Problem-local abstraction boundary for the concrete digit scanner.
module UNIQUE-DIGITS-WITH-HELPER
  imports UNIQUE-DIGITS-BASE

  rule <k>
         #applyK(
           toCall(closureVal(("n", .ParamNames), oddDigitsBody, 0)),
           (N:Int, .Vals))
         => oddDigits(N)
       ... </k>
    [priority(40)]
endmodule

// Problem-local summary for the source-level filter loop.  It connects the
// concrete accumulator heap object to the opaque digit predicate above.
module UNIQUE-DIGITS-VERIFICATION
  imports UNIQUE-DIGITS-WITH-HELPER

  rule <k>
         #loop(list(INPUT:ValSeq), Name("n"), filterLoopBody)
         => .K
       ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("n" |-> OLD:Val
            "result" |-> ref(H:Int)
            "x" |-> X:Val)
           =>
           ("n" |-> lastInput(OLD, INPUT)
            "result" |-> ref(H)
            "x" |-> X),
           P:Parent) ...
       </scopes>
       <heap>
         ... H |-> list(ACC:ValSeq => filterOddAcc(ACC, INPUT)) ...
       </heap>
    [priority(40)]
endmodule
