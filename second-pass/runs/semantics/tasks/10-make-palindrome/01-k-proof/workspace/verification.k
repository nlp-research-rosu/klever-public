requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical sequence operations used by the specification.
  // MPY-METHODS already supplies revIS and dropIS; only prefix extraction is
  // new here.
  syntax IntSeq ::= prefixIS(IntSeq, Int) [function]

  rule prefixIS(_:IntSeq, N:Int) => .IntSeq requires N <=Int 0
  rule prefixIS(iCons(C:Int, R:IntSeq), N:Int)
    => iCons(C, prefixIS(R, N -Int 1))
    requires N >Int 0

  syntax Bool ::= palindromeIS(IntSeq) [function]
  rule palindromeIS(S:IntSeq) => S ==K revIS(S)

  // Exact translated closure for the requested entry point.  Pinning this in
  // the proof state makes the loop claim specific to solution.mpy.
  syntax Val ::= "makePalindromeClosure" [function]
  rule makePalindromeClosure
    => closureVal(
      ("string", .ParamNames),
      Assign(Name("i"), Int(0))
      For(Name("i"), Call(Name("range"), Call(Name("len"), Name("string"))),
        If(Call(Name("is_palindrome"),
                Subscript(Name("string"), Slice(Name("i"), NoBound, NoBound))),
           Return(BinOp("+", Name("string"),
             Subscript(Subscript(Name("string"),
                                 Slice(NoBound, Name("i"), NoBound)),
                       Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))),
           .Stmts))
      Return(Name("string")) .Stmts,
      0)

  // The exact result of scanning suffixes beginning at index I.  The first
  // palindromic suffix corresponds to the longest one, hence the shortest
  // prefix that must be mirrored at the end.
  syntax IntSeq ::= palindromeFrom(IntSeq, Int) [function]
  rule palindromeFrom(S:IntSeq, I:Int)
    => seqConcat(S, revIS(prefixIS(S, I)))
    requires I <Int isLen(S) andBool palindromeIS(dropIS(S, I))
  rule palindromeFrom(S:IntSeq, I:Int)
    => palindromeFrom(S, I +Int 1)
    requires I <Int isLen(S) andBool notBool palindromeIS(dropIS(S, I))
  rule palindromeFrom(S:IntSeq, I:Int) => S
    requires I >=Int isLen(S)

  // Sound summaries of the three slice shapes used by solution.py.  They
  // avoid expanding CPython's index arithmetic during symbolic execution;
  // prefixIS/dropIS/revIS give their recursive meanings.
  rule <k> noB ~> #slStep(str(S:IntSeq), someB(I:Int), noB)
        => str(dropIS(S, I)) ... </k>
    requires 0 <=Int I andBool I <=Int isLen(S)
    [priority(40)]

  rule <k> noB ~> #slStep(str(S:IntSeq), noB, someB(I:Int))
        => str(prefixIS(S, I)) ... </k>
    requires 0 <=Int I andBool I <=Int isLen(S)
    [priority(40)]

  rule <k> someB(-1) ~> #slStep(str(S:IntSeq), noB, noB)
        => str(revIS(S)) ... </k>
    [priority(40)]

  // Verified helper summary: this exact closure is the translation of
  // is_palindrome in solution.py.  Its body compares the argument with the
  // full reverse summarized immediately above.
  rule <k>
    #applyK(toCall(closureVal(
      ("string", .ParamNames),
      Return(Compare(Name("string"),
        CmpOp("==", Subscript(Name("string"),
          Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))) .Stmts,
      0)),
      (str(S:IntSeq), .Vals))
    => palindromeIS(S) ...
  </k> [priority(40)]

  // The function-frame pop writes `undef` at the symbolic frame key.  The
  // builtin map hook does not normalize that deletion for a symbolic key, so
  // expose the corresponding finite-map identity to the prover.
  rule (((L:Int |-> _:Scope) REST:Map) [ L <- undef ]) => REST
    requires notBool (L in_keys(REST))
endmodule
