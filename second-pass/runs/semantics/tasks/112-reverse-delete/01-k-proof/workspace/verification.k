requires "reference-semantics/semantics.k"

module MPY-VERIFICATION-BASE
  imports MPY

  // Process the remaining input left-to-right, appending each retained
  // character to the forward accumulator.
  syntax IntSeq ::= keptAcc(IntSeq, IntSeq, IntSeq) [function, total]
  rule keptAcc(.IntSeq, _:IntSeq, A:IntSeq) => A
  rule keptAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, A:IntSeq)
    => keptAcc(XS, C, A)
    requires strContains(iCons(X, .IntSeq), C)
    [simplification]
  rule keptAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, A:IntSeq)
    => keptAcc(XS, C, seqConcat(A, iCons(X, .IntSeq)))
    requires notBool strContains(iCons(X, .IntSeq), C)
    [simplification]

  // The implementation constructs the reverse incrementally by prepending.
  syntax IntSeq ::= reversedKeptAcc(IntSeq, IntSeq, IntSeq) [function, total]
  rule reversedKeptAcc(.IntSeq, _:IntSeq, A:IntSeq) => A
  rule reversedKeptAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, A:IntSeq)
    => reversedKeptAcc(XS, C, A)
    requires strContains(iCons(X, .IntSeq), C)
    [simplification]
  rule reversedKeptAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, A:IntSeq)
    => reversedKeptAcc(XS, C, iCons(X, A))
    requires notBool strContains(iCons(X, .IntSeq), C)
    [simplification]

  // A for-loop leaves its target bound to the last element, or unchanged
  // when the iterable is empty.
  syntax Val ::= lastCharacter(IntSeq, Val) [function, total]
  rule lastCharacter(.IntSeq, V:Val) => V
  rule lastCharacter(iCons(X:Int, XS:IntSeq), _:Val)
    => lastCharacter(XS, str(iCons(X, .IntSeq)))
endmodule

module MPY-VERIFICATION
  imports MPY-VERIFICATION-BASE

  // This is the proved loop invariant from LOOP-SPEC, installed as a lemma
  // for the end-to-end entry-point proof in SPEC.
  rule
    <k>
      #loop(
        str(S:IntSeq),
        Name("character"),
        If(
          Compare(Name("character"), CmpOp("not in", Name("c"))),
          AugAssign(Name("result"), "+", Name("character"))
          Assign(
            Name("reversed_result"),
            BinOp("+", Name("character"), Name("reversed_result"))),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |->
        ( scope(
            ( "s" |-> str(ORIG:IntSeq)
              "c" |-> str(C:IntSeq)
              "result" |-> str(A:IntSeq)
              "reversed_result" |-> str(RA:IntSeq)
              "character" |-> V:Val ),
            P:Parent)
        => scope(
            ( "s" |-> str(ORIG)
              "c" |-> str(C)
              "result" |-> str(keptAcc(S, C, A))
              "reversed_result" |-> str(reversedKeptAcc(S, C, RA))
              "character" |-> lastCharacter(S, V) ),
            P) )
      ...
    </scopes>
    [priority(40)]
endmodule
