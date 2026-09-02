requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact syntactic abbreviations for the translated Python body.
  syntax Stmts ::= filterBody() [macro]
  rule filterBody()
    => If(
         Compare(Name("num"), CmpOp(">", Int(10))),
         Assign(Name("text"), Call(Name("str"), Name("num")))
         If(
           Compare(
             BinOp(
               "%",
               Call(Name("ord"), Subscript(Name("text"), Int(0))),
               Int(2)),
             CmpOp("==", Int(1))),
           If(
             Compare(
               BinOp(
                 "%",
                 Call(
                   Name("ord"),
                   Subscript(Name("text"), UnaryOp("-", Int(1)))),
                 Int(2)),
               CmpOp("==", Int(1))),
             AugAssign(Name("count"), "+", Int(1)),
             .Stmts),
           .Stmts),
         .Stmts)

  syntax Stmts ::= specialFilterStmts() [macro]
  rule specialFilterStmts()
    => Assign(Name("count"), Int(0))
       Assign(Name("num"), Int(0))
       Assign(Name("text"), Str(""))
       For(Name("num"), Name("nums"), filterBody())
       Return(Name("count"))

  // The contract domain: arbitrary finite Python lists whose values are Ints.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq))
    => isInt(V) andBool allInts(REST)

  // Guarded total projection from the dynamic Val sort to Int. This is the
  // standard K total-projection pattern: it is connected to the built-in
  // partial subsort cast and can only be used while isInt(V) is entailed.
  syntax Bool ::= definedProjectInt(Val) [function, total]
  rule definedProjectInt(V:Val) => isInt(V)

  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Int)
    => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectIntTotal(V:Val) => {V}:>Int
    requires definedProjectInt(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Int => projectIntTotal(V)
    requires definedProjectInt(V)
    [symbolic(V), simplification, preserves-definedness]

  rule projectIntTotal(N:Int) => N [simplification]
  rule projectIntTotal(projectIntTotal(V:Val))
    => projectIntTotal(V)
    [simplification]

  // Guarded dispatch twins of the exact frozen-semantics equations used by the
  // program when a dynamically sorted list element is known to be an Int.
  rule applyCmp(">", V:Val, I:Int)
    => projectIntTotal(V) >Int I
    requires definedProjectInt(V)
    [simplification]

  rule applyBuiltin("str", V:Val, .Vals)
    => str(strToCodes(Int2String(projectIntTotal(V))))
    requires definedProjectInt(V)
    [simplification]

  // Decimal character codes used by the implementation. Int2String is the
  // fixed K STRING operation used by the supplied Python str(int) semantics.
  syntax Int ::= firstDecimalCode(Int) [function, total]
               | lastDecimalCode(Int)  [function, total]
  rule firstDecimalCode(N:Int)
    => intSeqAt(strToCodes(Int2String(N)), 0)
  rule lastDecimalCode(N:Int)
    => intSeqAt(
         strToCodes(Int2String(N)),
         -1 +Int isLen(strToCodes(Int2String(N))))

  syntax Bool ::= isSpecial(Int) [function, total]
                | firstDigitOdd(Int) [function, total]
                | lastDigitOdd(Int)  [function, total]
  rule firstDigitOdd(N:Int)
    => pyMod(firstDecimalCode(N), 2) ==Int 1
  rule lastDigitOdd(N:Int)
    => pyMod(lastDecimalCode(N), 2) ==Int 1
  rule isSpecial(N:Int)
    => N >Int 10
       andBool firstDigitOdd(N)
       andBool lastDigitOdd(N)

  // Mathematical count of qualifying elements in an arbitrary finite input.
  syntax Int ::= specialCount(ValSeq) [function, total]
  rule specialCount(.ValSeq) => 0 [simplification]
  rule specialCount(vCons(V:Val, REST:ValSeq))
    => 1 +Int specialCount(REST)
    requires definedProjectInt(V)
     andBool projectIntTotal(V) >Int 10
     andBool firstDigitOdd(projectIntTotal(V))
     andBool lastDigitOdd(projectIntTotal(V))
    [simplification]
  rule specialCount(vCons(V:Val, REST:ValSeq))
    => specialCount(REST)
    requires definedProjectInt(V)
     andBool notBool (projectIntTotal(V) >Int 10)
    [simplification]
  rule specialCount(vCons(V:Val, REST:ValSeq))
    => specialCount(REST)
    requires definedProjectInt(V)
     andBool projectIntTotal(V) >Int 10
     andBool notBool firstDigitOdd(projectIntTotal(V))
    [simplification]
  rule specialCount(vCons(V:Val, REST:ValSeq))
    => specialCount(REST)
    requires definedProjectInt(V)
     andBool projectIntTotal(V) >Int 10
     andBool firstDigitOdd(projectIntTotal(V))
     andBool notBool lastDigitOdd(projectIntTotal(V))
    [simplification]
  rule specialCount(vCons(V:Val, REST:ValSeq))
    => specialCount(REST)
    requires notBool definedProjectInt(V)
    [simplification]
endmodule
