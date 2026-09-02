requires "reference-semantics/semantics.k"

module FACTORIZE-VERIFICATION
  imports MPY

  // The exact statement blocks emitted for factorize by py2mpy.py.
  syntax Stmts ::= "factorizeStep" [macro]
  rule factorizeStep
    => If(
         Compare(BinOp("%", Name("n"), Name("divisor")),
                 CmpOp("==", Int(0))),
         Expr(Call(Attribute(Name("factors"), "append"), Name("divisor")))
         Assign(Name("n"), BinOp("//", Name("n"), Name("divisor"))),
         AugAssign(Name("divisor"), "+", Int(1)))

  syntax Stmts ::= "factorizeBody" [macro]
  rule factorizeBody
    => Assign(Name("factors"), ListExpr(.Exprs))
       Assign(Name("divisor"), Int(3))
       While(Compare(Name("n"), CmpOp(">", Int(1))), factorizeStep)
       Return(Name("factors"))

  syntax Stmt ::= "factorizeDef" [macro]
  rule factorizeDef
    => FuncDef("factorize", Params("n"), factorizeBody)

  // Canonical smallest-trial-divisor factorization, with an accumulator.
  // For positive N, the first divisor encountered is prime; retaining D after
  // division records multiplicity, while incrementing D preserves ordering.
  syntax ValSeq ::= factorLoop(Int, Int, ValSeq) [function]
  rule factorLoop(N:Int, _D:Int, VS:ValSeq) => VS
    requires N <=Int 1
  rule factorLoop(N:Int, D:Int, VS:ValSeq)
    => factorLoop((N -Int pyMod(N, D)) /Int D, D,
                  valSeqConcat(VS, vCons(D, .ValSeq)))
    requires N >Int 1 andBool D >Int 0
         andBool pyMod(N, D) ==Int 0
  rule factorLoop(N:Int, D:Int, VS:ValSeq)
    => factorLoop(N, D +Int 1, VS)
    requires N >Int 1 andBool D >Int 0
         andBool pyMod(N, D) =/=Int 0

  syntax ValSeq ::= primeFactors(Int) [function]
  rule primeFactors(N:Int) => factorLoop(N, 2, .ValSeq)

  // Final divisor value, used only to state the complete loop-frame invariant.
  syntax Int ::= factorDivisor(Int, Int) [function]
  rule factorDivisor(N:Int, D:Int) => D
    requires N <=Int 1
  rule factorDivisor(N:Int, D:Int)
    => factorDivisor((N -Int pyMod(N, D)) /Int D, D)
    requires N >Int 1 andBool D >Int 0
         andBool pyMod(N, D) ==Int 0
  rule factorDivisor(N:Int, D:Int)
    => factorDivisor(N, D +Int 1)
    requires N >Int 1 andBool D >Int 0
         andBool pyMod(N, D) =/=Int 0
endmodule

// This module is used only after FACTORIZE-LOOP-SPEC.factorize-loop has been
// proved against FACTORIZE-VERIFICATION.  The rule is textually the proved
// claim, promoted to a lemma so the entry-point proof need not repeat the
// expensive generic reachability-claim matching.
module FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA
  imports FACTORIZE-VERIFICATION

  rule
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(1))), factorizeStep)
      ~> KONT
      => KONT
    </k>
    <env> L </env>
    <scopes>
      (L |-> scope(
        ("n" |-> N
         "divisor" |-> D
         "factors" |-> ref(H)),
        parent(0)))
      SC
      =>
      (L |-> scope(
        ("n" |-> 1
         "divisor" |-> factorDivisor(N, D)
         "factors" |-> ref(H)),
        parent(0)))
      SC
    </scopes>
    <heap>
      (H |-> list(VS)) HP
      => (H |-> list(factorLoop(N, D, VS))) HP
    </heap>
    requires N >=Int 1 andBool D >=Int 2
    [priority(40), label(factorize-loop-lemma)]
endmodule
