requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // This is the exact translated body of decode_cyclic in solution.mpy.
  syntax Stmts ::= "decodeBody" [macro]
  rule decodeBody =>
    Expr(
      Str(
        "\n    takes as input string encoded with encode_cyclic function. Returns decoded string.\n    "))
    If(Compare(Call(Name("len"), Name("s")), CmpOp("<", Int(3))),
      Return(Name("s")),
      .Stmts)
    Return(
      BinOp(
        "+",
        BinOp(
          "+",
          Subscript(Name("s"), Int(2)),
          Subscript(Name("s"), Slice(NoBound, Int(2), NoBound))),
        Call(
          Name("decode_cyclic"),
          Subscript(Name("s"), Slice(Int(3), NoBound, NoBound)))))

  syntax Val ::= "decodeClosure" [macro]
  rule decodeClosure => closureVal("s", decodeBody, 0)

  // Independent recursive specification: rotate every complete block of
  // three codes to the right, and preserve a final block of length < 3.
  // It is phrased with the semantics' sequence primitives so that symbolic
  // (not yet constructor-split) IntSeq values can reduce under a length path
  // condition.
  syntax IntSeq ::= decodeCodes(IntSeq) [function, total]
  rule decodeCodes(CS:IntSeq) => CS
    requires isLen(CS) <Int 3
  rule decodeCodes(CS:IntSeq)
    => seqConcat(
         seqConcat(
           iCons(intSeqAt(CS, 2), .IntSeq),
           buildIS(CS, 0, 2, 1)),
         decodeCodes(buildIS(CS, 3, isLen(CS), 1)))
    requires isLen(CS) >=Int 3

  // Symbolic slice-length lemma for s[3:]. It is a derived fact about
  // buildIS: with unit step and stop=len(s), exactly len(s)-3 codes remain.
  rule isLen(buildIS(CS:IntSeq,
                     clampHi(3, isLen(CS), 1),
                     isLen(CS),
                     1))
    => isLen(CS) -Int 3
    requires isLen(CS) >=Int 3
    [simplification]

  rule clampHi(3, isLen(CS:IntSeq), 1) => 3
    requires isLen(CS) >=Int 3
    [simplification]

  // Scope locations are allocated monotonically. keysBelow records the
  // corresponding invariant for the abstract remainder of a scopes map.
  syntax Bool ::= keysBelow(Map, Int) [function]
  rule keysBelow(.Map, _N:Int) => true
  rule keysBelow((I:Int |-> _S:Scope) REST:Map, N:Int)
    => (I <Int N) andBool keysBelow(REST, N)

  rule keysBelow(M:Map, N:Int +Int 1) => true
    requires keysBelow(M, N)
    [simplification]

  rule N:Int in_keys(M:Map) => false
    requires keysBelow(M, N)
    [simplification]

  rule (M:Map [ N:Int <- S:Scope ]) => (N |-> S) M
    requires keysBelow(M, N)
    [simplification]

  rule (((N:Int |-> _S:Scope) M:Map) [ N <- undef]) => M
    requires keysBelow(M, N)
    [simplification]
endmodule
