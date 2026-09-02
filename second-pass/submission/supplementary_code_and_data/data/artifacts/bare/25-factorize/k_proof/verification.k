requires "semantic.k"

module SOLUTION-PROGRAM
  imports SEMANTIC

  // This is the parsed term emitted in solution.mpy.  Keeping it as a K term
  // makes the proof about the translator's output, not about Python source text.
  syntax Module ::= SolutionModule() [function]
  rule SolutionModule() =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("factorize_from", Params("n", "divisor"),
        If(Compare(Name("n"), CmpOp("<", Int(2))),
          Return(ListExpr(.Exprs)),
          .Stmts)
        If(Compare(BinOp("*", Name("divisor"), Name("divisor")),
                   CmpOp(">", Name("n"))),
          Return(ListExpr(Name("n"))),
          .Stmts)
        If(Compare(BinOp("%", Name("n"), Name("divisor")),
                   CmpOp("==", Int(0))),
          Return(BinOp("+",
            ListExpr(Name("divisor")),
            Call(Name("factorize_from"),
              BinOp("//", Name("n"), Name("divisor")),
              Name("divisor")))),
          .Stmts)
        Return(Call(Name("factorize_from"),
          Name("n"), BinOp("+", Name("divisor"), Int(1)))))
      FuncDef("factorize", Params("n"),
        Return(Call(Name("factorize_from"), Name("n"), Int(2)))))

  syntax Map ::= SolutionFunctions() [function]
  rule SolutionFunctions() => collectStmts(SolutionModule())

  syntax MachineState ::= SolutionMachine(Int) [function]
  rule SolutionMachine(N) =>
    Machine(Invoke("factorize", ListItem(IntVal(N))) ~> Finish,
            .Map, SolutionFunctions(), .List, noResult)

  syntax Map ::= collectStmts(Module) [function]
  rule collectStmts(Module(SS)) => collect(SS)
endmodule

module VERIFICATION
  imports SOLUTION-PROGRAM

  // Mathematical trial-division specification.  D is the next candidate.
  // The first rule covers the conventional factorization of 1 as the empty
  // list.  The other rules either emit a divisor or advance the candidate.
  syntax Val ::= FactorFrom(Int, Int) [function]
  rule FactorFrom(N, _) => ListVal(.List)
    requires N <Int 2
  rule FactorFrom(N, D) => ListVal(ListItem(IntVal(N)))
    requires N >=Int 2 andBool D >=Int 2 andBool D *Int D >Int N
  rule FactorFrom(N, D)
    => PrependFactor(D, FactorFrom(N /Int D, D))
    requires N >=Int 2 andBool D >=Int 2
             andBool D *Int D <=Int N andBool N %Int D ==Int 0
  rule FactorFrom(N, D)
    => FactorFrom(N, D +Int 1)
    requires N >=Int 2 andBool D >=Int 2
             andBool D *Int D <=Int N andBool N %Int D =/=Int 0

  syntax Val ::= FactorizeSpec(Int) [function]
  rule FactorizeSpec(N) => FactorFrom(N, 2)

  syntax Val ::= PrependFactor(Int, Val) [function]
  rule PrependFactor(D, ListVal(L))
    => ListVal(ListItem(IntVal(D)) L)

  // Observable contract helpers used by claims in spec.k.
  syntax Int ::= Product(Val) [function]
  rule Product(ListVal(.List)) => 1
  rule Product(ListVal(ListItem(IntVal(X)) REST))
    => X *Int Product(ListVal(REST))

  // OrderedFrom(V, L) says that V's integer elements are nondecreasing and
  // that its first element, if present, is at least L.
  syntax Bool ::= OrderedFrom(Val, Int) [function]
  rule OrderedFrom(ListVal(.List), _) => true
  rule OrderedFrom(ListVal(ListItem(IntVal(X)) REST), L)
    => (L <=Int X) andBool OrderedFrom(ListVal(REST), X)

  syntax Val ::= MachineValue(MachineState) [function]
  rule MachineValue(Halted(_, _, _, V)) => V

  syntax Bool ::= HasDivisor(Int, Int) [function]
  rule HasDivisor(N, D) => false
    requires D *Int D >Int N
  rule HasDivisor(N, D) => true
    requires D *Int D <=Int N andBool N %Int D ==Int 0
  rule HasDivisor(N, D) => HasDivisor(N, D +Int 1)
    requires D *Int D <=Int N andBool N %Int D =/=Int 0

  syntax Bool ::= IsPrime(Int) [function]
  rule IsPrime(N) => (N >=Int 2) andBool notBool HasDivisor(N, 2)

  syntax Bool ::= AllPrime(Val) [function]
  rule AllPrime(ListVal(.List)) => true
  rule AllPrime(ListVal(ListItem(IntVal(X)) REST))
    => IsPrime(X) andBool AllPrime(ListVal(REST))

  syntax Bool ::= ValidFactorization(Int, Val) [function]
  rule ValidFactorization(N, V)
    => (Product(V) ==Int N)
       andBool OrderedFrom(V, 2)
       andBool AllPrime(V)

  syntax Observation ::= Observe(Bool)
endmodule
