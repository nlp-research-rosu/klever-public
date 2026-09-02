requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact syntax aliases for the three loop bodies and the translated
  // function body.  These aliases only keep the claims readable.
  syntax Stmts ::= "primeLoopBody" [function, total]
  rule primeLoopBody
    => If(
         Compare(
           BinOp("%", Name("value"), Name("divisor")),
           CmpOp("==", Int(0))),
         Assign(Name("candidate"), Bool(false)),
         .Stmts)
       AugAssign(Name("divisor"), "+", Int(1))

  syntax Stmts ::= "scanBody" [function, total]
  rule scanBody
    => If(
         Compare(Name("value"), CmpOp(">", Name("largest"))),
         Assign(
           Name("candidate"),
           Compare(Name("value"), CmpOp(">=", Int(2))))
         Assign(Name("divisor"), Int(2))
         While(
           Compare(Name("divisor"), CmpOp("<", Name("value"))),
           primeLoopBody)
         If(
           Name("candidate"),
           Assign(
             Name("largest"),
             BinOp("+", Name("value"), Int(0))),
           .Stmts),
         .Stmts)

  syntax Stmts ::= "digitLoopBody" [function, total]
  rule digitLoopBody
    => AugAssign(
         Name("total"),
         "+",
         BinOp("%", Name("largest"), Int(10)))
       AugAssign(Name("largest"), "//", Int(10))

  syntax Stmts ::= "targetBody" [function, total]
  rule targetBody
    => Assign(Name("largest"), Int(0))
       Assign(Name("value"), Int(0))
       Assign(Name("candidate"), Bool(false))
       Assign(Name("divisor"), Int(2))
       For(Name("value"), Name("lst"), scanBody)
       Assign(Name("total"), Int(0))
       While(
         Compare(Name("largest"), CmpOp(">", Int(0))),
         digitLoopBody)
       Return(Name("total"))

  // The source contract restricts list elements to integers.  This predicate
  // carries that dynamic-language fact through symbolic ValSeq iteration.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, R:ValSeq))
    => isInt(V) andBool allInts(R)

  // Guarded total projection of a dynamically sorted Val known to be an Int.
  // This is the standard total-projection pattern: it does not invent a value;
  // it is usable only under the exact generated sort predicate.
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

  rule projectIntTotal(I:Int) => I [simplification]
  rule projectIntTotal(projectIntTotal(V:Val))
    => projectIntTotal(V)
    [simplification]

  // Guarded dispatch twins of the fixed MPY-INT equations used by the program.
  // Their match domain is exactly the original Int domain.
  rule applyCmp(">", V:Val, I:Int)
    => projectIntTotal(V) >Int I
    requires isInt(V)
    [simplification]

  rule applyCmp(">=", V:Val, I:Int)
    => projectIntTotal(V) >=Int I
    requires isInt(V)
    [simplification]

  rule applyCmp("<", I:Int, V:Val)
    => I <Int projectIntTotal(V)
    requires isInt(V)
    [simplification]

  rule applyBin("%", V:Val, I:Int)
    => pyMod(projectIntTotal(V), I)
    requires isInt(V)
    [simplification]

  rule applyBin("+", V:Val, I:Int)
    => projectIntTotal(V) +Int I
    requires isInt(V)
    [simplification]

  // No divisor in [D, N) divides N.  D < 2 is an unused totalization case.
  syntax Bool ::= primeTail(Int, Int) [function, total]
  rule primeTail(_N:Int, D:Int) => false
    requires D <Int 2
  rule primeTail(N:Int, D:Int) => true
    requires D >=Int 2 andBool D >=Int N
  rule primeTail(N:Int, D:Int)
    => notBool (pyMod(N, D) ==Int 0)
       andBool primeTail(N, D +Int 1)
    requires D >=Int 2 andBool D <Int N
    [concrete, simplification]

  // The recursive equation is oriented toward the summary during symbolic
  // proof, so a symbolic divisor does not trigger unbounded evaluator
  // unfolding.  These are the two disjoint step cases of that equation.
  rule primeTail(N:Int, D:Int) => false
    requires D >=Int 2
      andBool D <Int N
      andBool pyMod(N, D) ==Int 0
    [simplification]
  rule primeTail(N:Int, D:Int) => primeTail(N, D -Int 1)
    requires D >Int 2
      andBool D <=Int N
      andBool pyMod(N, D -Int 1) =/=Int 0
    [symbolic(N, D), simplification]

  syntax Bool ::= isPrime(Int) [function, total]
  rule isPrime(N:Int)
    => N >=Int 2 andBool primeTail(N, 2)

  // One scan step: retain M unless X is both larger and prime.
  syntax Int ::= selectPrime(Int, Int) [function, total]
  rule selectPrime(M:Int, X:Int) => X
    requires X >Int M andBool isPrime(X)
  rule selectPrime(M:Int, X:Int) => M
    requires notBool (X >Int M andBool isPrime(X))

  // Fold selectPrime across the complete symbolic input list.
  syntax Int ::= largestPrime(ValSeq, Int) [function, total]
  rule largestPrime(.ValSeq, M:Int) => M
  rule largestPrime(vCons(V:Val, R:ValSeq), M:Int)
    => largestPrime(R, selectPrime(M, projectIntTotal(V)))
    requires isInt(V)
  rule largestPrime(vCons(V:Val, R:ValSeq), M:Int)
    => largestPrime(R, M)
    requires notBool isInt(V)

  // Decimal digit sum for the nonnegative accumulator produced by the scan.
  syntax Int ::= digitSum(Int) [function, total]
  rule digitSum(N:Int) => 0
    requires N <=Int 0
  rule digitSum(N:Int)
    => pyMod(N, 10)
       +Int digitSum((N -Int pyMod(N, 10)) /Int 10)
    requires N >Int 0
    [concrete, simplification]
  rule pyMod(N:Int, 10)
       +Int digitSum((N -Int pyMod(N, 10)) /Int 10)
    => digitSum(N)
    requires N >Int 0
    [symbolic(N), simplification]
  rule ((N %Int 10 +Int 10) %Int 10)
       +Int digitSum(
         (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10)
    => digitSum(N)
    requires N >Int 0
    [symbolic(N), simplification]
  rule T:Int
       +Int ((N %Int 10 +Int 10) %Int 10)
       +Int digitSum(
         (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10)
    => T +Int digitSum(N)
    requires N >Int 0
    [symbolic(N), simplification]
endmodule
