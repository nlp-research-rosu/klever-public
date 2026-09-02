requires "reference-semantics/semantics.k"

module EVEN-ODD-VERIFICATION
  imports MPY

  // Mathematical specification: count character codes of each parity.
  // Decimal digit codes have the same parity as their represented digits
  // because the code for "0" is 48.
  syntax Int ::= evenDigits(IntSeq) [function, total]
               | oddDigits(IntSeq)  [function, total]

  rule evenDigits(.IntSeq) => 0
  rule evenDigits(iCons(C:Int, R:IntSeq)) =>
    (#if pyMod(C, 2) ==Int 0 #then 1 #else 0 #fi) +Int evenDigits(R)

  rule oddDigits(.IntSeq) => 0
  rule oddDigits(iCons(C:Int, R:IntSeq)) =>
    (#if pyMod(C, 2) ==Int 0 #then 0 #else 1 #fi) +Int oddDigits(R)

  // The loop target is deliberately initialized in solution.py.  Tracking its
  // final value makes the loop invariant describe the full local scope.
  syntax Val ::= lastSeen(IntSeq, Val) [function, total]
  rule lastSeen(.IntSeq, D:Val) => D
  rule lastSeen(iCons(C:Int, R:IntSeq), _:Val) =>
    lastSeen(R, str(iCons(C, .IntSeq)))

  syntax Stmts ::= "#digitLoopBody" [macro]
  rule #digitLoopBody =>
    If(
      Compare(
        BinOp("%", Call(Name("ord"), Name("digit")), Int(2)),
        CmpOp("==", Int(0))),
      AugAssign(Name("even_count"), "+", Int(1)),
      AugAssign(Name("odd_count"), "+", Int(1)))

  syntax Stmts ::= "#evenOddFunctionBody" [macro]
  rule #evenOddFunctionBody =>
    Expr(Str("Return the counts of even and odd decimal digits in num."))
    Assign(Name("even_count"), Int(0))
    Assign(Name("odd_count"), Int(0))
    Assign(Name("digit"), Int(0))
    For(
      Name("digit"),
      Call(Name("str"), Call(Name("abs"), Name("num"))),
      #digitLoopBody)
    Return(TupleExpr(Name("even_count"), Name("odd_count")))

  syntax Scope ::= "#evenOddModuleScope" [macro]
  rule #evenOddModuleScope =>
    scope(
      "even_odd_count" |->
        closureVal(("num", .ParamNames), #evenOddFunctionBody, 0),
      parent(-1))
endmodule

// This module contains the compositional loop summary used by the entry-point
// theorem.  Its identical reachability claim is proved first against the base
// module (where this rule is absent).
module EVEN-ODD-VERIFICATION-SUMMARY
  imports EVEN-ODD-VERIFICATION

  rule
    <k>
      #loop(str(CS:IntSeq), Name("digit"), #digitLoopBody)
      ~> CONT:K
    =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        "num"        |-> N:Int
        "even_count" |-> E:Int
        "odd_count"  |-> O:Int
        "digit"      |-> D:Val,
        parent(0))
    =>
      1  |-> scope(
        "num"        |-> N
        "even_count" |-> E +Int evenDigits(CS)
        "odd_count"  |-> O +Int oddDigits(CS)
        "digit"      |-> lastSeen(CS, D),
        parent(0))
      ...
    </scopes>
    [priority(40)]
endmodule
