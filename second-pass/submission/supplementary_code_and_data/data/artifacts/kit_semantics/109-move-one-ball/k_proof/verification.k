requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // Exact AST aliases for solution.mpy.  These are compile-time macros: the
  // fixed MPY rules still execute every statement in the function and loop.
  syntax Stmts ::= "scanBody" [macro]
  rule scanBody
    => Assign(Name("drops"),
         BinOp("+", Name("drops"),
           Compare(Name("current"), CmpOp("<", Name("previous")))))
       Assign(Name("previous"), Name("current"))

  syntax Stmts ::= "moveOneBallBody" [macro]
  rule moveOneBallBody
    => If(UnaryOp("not", Name("arr")),
          Return(Bool(true)),
          .Stmts)
       Assign(Name("first"), Subscript(Name("arr"), Int(0)))
       Assign(Name("previous"), Name("first"))
       Assign(Name("current"), Name("first"))
       Assign(Name("drops"), Int(0))
       For(Name("current"), Name("arr"), scanBody)
       Assign(Name("drops"),
         BinOp("+", Name("drops"),
           Compare(Name("first"), CmpOp("<", Name("previous")))))
       Return(Compare(Name("drops"), CmpOp("<=", Int(1))))

  // The formal input-domain predicate: every MPY list element is an Int.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq)                => true
  rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R)

  // Sort-refinement lemma for the fixed MPY-INT comparison equation.  The
  // guard states exactly when both Val-sorted operands are Int injections.
  rule applyCmp("<", A:Val, B:Val)
    => {A}:>Int <Int {B}:>Int
    requires isInt(A) andBool isInt(B)
    [simplification]

  // The exact left fold performed by the loop.  These equations are
  // intentionally defined only on the allInts domain.
  syntax Int ::= scanDrops(Int, Val, ValSeq) [function]
  rule scanDrops(D:Int, _:Val, .ValSeq) => D
  rule scanDrops(D:Int, P:Val, vCons(V:Val, R:ValSeq))
    => scanDrops(
         D +Int (#if {V}:>Int <Int {P}:>Int #then 1 #else 0 #fi),
         V,
         R)
    requires isInt(P) andBool isInt(V)

  // The final integer after scanning VS, or P if VS is empty.
  syntax Val ::= lastAfter(Val, ValSeq) [function, total]
  rule lastAfter(P:Val, .ValSeq)                => P
  rule lastAfter(_:Val, vCons(V:Val, R:ValSeq)) => lastAfter(V, R)

  rule applyCmp("<", A:Val, lastAfter(P:Val, VS:ValSeq))
    => {A}:>Int <Int {lastAfter(P, VS)}:>Int
    requires isInt(A) andBool isInt(P) andBool allInts(VS)
    [simplification]

  // Exact result property: empty is accepted; a nonempty circular sequence is
  // accepted iff it has at most one strict circular descent.
  syntax Bool ::= moveSpec(ValSeq) [function]
  rule moveSpec(VS:ValSeq) => true
    requires VS ==K .ValSeq
  rule moveSpec(VS:ValSeq)
    => scanDrops(0, valSeqAt(VS, 0), VS)
       +Int (#if {valSeqAt(VS, 0)}:>Int
                   <Int {lastAfter(valSeqAt(VS, 0), VS)}:>Int
             #then 1 #else 0 #fi)
       <=Int 1
    requires notBool (VS ==K .ValSeq) andBool allInts(VS)
endmodule
