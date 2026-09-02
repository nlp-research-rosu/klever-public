requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // Let symbolic Boolean conditions split the same way concrete true/false
  // conditions do. The reference rules already handle ground Booleans.
  rule <k> #branch(C:Bool, T:Stmts, _:Stmts) => T ... </k>
       requires C
  rule <k> #branch(C:Bool, _:Stmts, E:Stmts) => E ... </k>
       requires notBool C

  // A total, structural name for s[1:]. This proof-side equation is exactly
  // the CPython-clamped unit-step slice for both empty and nonempty strings.
  syntax IntSeq ::= dropOne(IntSeq) [function, total]
  rule dropOne(.IntSeq)                 => .IntSeq
  rule dropOne(iCons(_:Int, R:IntSeq)) => R

  rule <k>
    Subscript(
      str(S:IntSeq),
      Slice(Int(1), NoBound, NoBound))
    => str(dropOne(S))
    ...
  </k>
  [priority(30)]

  // Search one current pattern per remaining character.  On a failed match,
  // moving the iterator's current character to the end is the next rotation.
  // Structural recursion on REM is what makes the loop proof inductive.
  syntax Bool ::= rotationsLoop(IntSeq, IntSeq, IntSeq) [function, total]
  rule rotationsLoop(_:IntSeq, _:IntSeq, .IntSeq) => false
       [simplification]
  rule rotationsLoop(A:IntSeq, P:IntSeq, iCons(_:Int, _:IntSeq)) => true
       requires strContains(P, A)
       [simplification]
  rule rotationsLoop(A:IntSeq, P:IntSeq, iCons(C:Int, R:IntSeq))
    => rotationsLoop(
         A,
         seqConcat(dropOne(P), iCons(C, .IntSeq)),
         R)
       requires notBool strContains(P, A)
       [simplification]
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // This is the proved SPEC-LEMMA.loop-invariant reachability summary,
  // promoted only for the second-stage entry-point proof.
  rule
    <k>
      #loop(
        str(REM),
        Name("char"),
        If(
          Compare(Name("pattern"), CmpOp("in", Name("a"))),
          Return(Bool(true)),
          .Stmts)
        Assign(
          Name("pattern"),
          BinOp(
            "+",
            Subscript(
              Name("pattern"),
              Slice(Int(1), NoBound, NoBound)),
            Name("char")))
        .Stmts)
      ~> (Return(Bool(false)) .Stmts)
      ~> #endcall
    =>
      rotationsLoop(A, P, REM)
      ~> CONT
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
         ("a" |-> str(A))
         ("b" |-> str(B))
         ("char" |-> str(CH))
         ("pattern" |-> str(P)),
         parent(0))
       0 |-> scope(G, parent(-1))
       -1 |-> BS:Scope)
    =>
      (0 |-> scope(G, parent(-1))
       -1 |-> BS)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <stack>
      (ListItem(frame(CONT:K, 0, 1)) REST:List => REST)
    </stack>
    <ret> noRet </ret>
    [priority(30)]
endmodule
