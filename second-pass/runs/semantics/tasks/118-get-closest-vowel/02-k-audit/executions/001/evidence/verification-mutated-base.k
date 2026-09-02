requires "reference-semantics/semantics.k"

module HUMAN-EVAL-118-VERIFICATION
  imports MPY

  // The exact function body generated in solution.mpy.
  syntax Stmts ::= "getClosestBody" [macro]
  rule getClosestBody
    => If(Compare(Call(Name("len"), Name("word")), CmpOp("<", Int(3))),
          Return(Str("a")),
          .Stmts)
       Assign(Name("result"),
         Call(Name("get_closest_vowel"),
              Subscript(Name("word"), Slice(Int(1), NoBound, NoBound))))
       If(Name("result"),
          Return(Name("result")),
          .Stmts)
       If(BoolOp("and",
            Compare(Subscript(Name("word"), Int(1)),
                    CmpOp("in", Str("AEIOUaeiou"))),
            Compare(Subscript(Name("word"), Int(0)),
                    CmpOp("not in", Str("AEIOUaeiou"))),
            Compare(Subscript(Name("word"), Int(2)),
                    CmpOp("not in", Str("AEIOUaeiou")))),
          Return(Subscript(Name("word"), Int(1))),
          .Stmts)
       Return(Str(""))
       .Stmts

  // A code-level statement of the contract.  closestVowelSpec returns either
  // the empty code sequence or the singleton code sequence of the rightmost
  // qualifying vowel.
  syntax Bool ::= isVowelCode(Int) [function, total]
  rule isVowelCode(C:Int)
    => C ==Int 65 orBool C ==Int 69 orBool C ==Int 73
       orBool C ==Int 79 orBool C ==Int 85
       orBool C ==Int 97 orBool C ==Int 101 orBool C ==Int 105
       orBool C ==Int 111 orBool C ==Int 117

  syntax Bool ::= qualifyingTriple(Int, Int, Int) [function, total]
  rule qualifyingTriple(A:Int, B:Int, C:Int)
    => notBool isVowelCode(A)
       andBool isVowelCode(B)
       andBool notBool isVowelCode(C)

  // This reference scans the tail first.  A nonempty tail result is therefore
  // already the rightmost answer; only an empty tail permits the current
  // three-character window to contribute its middle character.
  syntax IntSeq ::= closestVowelSpec(IntSeq) [function, total]
  rule closestVowelSpec(CS:IntSeq) => .IntSeq
    requires isLen(CS) <Int 3
  rule closestVowelSpec(.IntSeq) => .IntSeq
  rule closestVowelSpec(iCons(_:Int, .IntSeq)) => .IntSeq
  rule closestVowelSpec(iCons(_:Int, iCons(_:Int, .IntSeq))) => .IntSeq
  rule closestVowelSpec(iCons(A:Int, iCons(B:Int, iCons(C:Int, R:IntSeq))))
    => closestVowelSpec(iCons(B, iCons(C, R)))
    requires closestVowelSpec(iCons(B, iCons(C, R))) =/=K .IntSeq
  rule closestVowelSpec(iCons(A:Int, iCons(B:Int, iCons(C:Int, R:IntSeq))))
    => iCons(B, .IntSeq)
    requires closestVowelSpec(iCons(B, iCons(C, R))) ==K .IntSeq
     andBool qualifyingTriple(A, B, C)
  rule closestVowelSpec(iCons(A:Int, iCons(B:Int, iCons(C:Int, R:IntSeq))))
    => .IntSeq
    requires closestVowelSpec(iCons(B, iCons(C, R))) ==K .IntSeq
     andBool notBool qualifyingTriple(A, B, C)

  // Valid for every nonempty string: Python's [1:] slice is its code tail.
  // This proof lemma avoids expanding buildIS one index at a time.
  rule <k> Subscript(str(iCons(_:Int, R:IntSeq)),
                     Slice(Int(1), NoBound, NoBound))
        => str(R) ... </k>
       [priority(40)]

  syntax IntSeq ::= "vowelCodes" [macro]
  rule vowelCodes
    => iCons(65, iCons(69, iCons(73, iCons(79, iCons(85,
       iCons(97, iCons(101, iCons(105, iCons(111, iCons(117,
       .IntSeq))))))))))

  rule strContains(iCons(C:Int, .IntSeq), vowelCodes)
    => isVowelCode(C)

  // Induction cutpoint for the strictly shorter recursive call.  The public
  // call starts in module frame 0 and is fully executed; only an application
  // made from inside that active function frame may use the induction
  // hypothesis.
  rule <k> #applyK(
              toCall(closureVal("word", getClosestBody, 0)),
              (str(CS:IntSeq), .Vals))
        => str(closestVowelSpec(CS)) ... </k>
       <env> L:Int </env>
       requires L >Int 0
       [priority(40)]

  // Structural lengths are natural numbers.  The backend otherwise treats
  // isLen of an opaque tail as an arbitrary mathematical integer.
  rule isLen(CS:IntSeq) <Int 0 => false [simplification]
  rule isLen(CS:IntSeq) >=Int 0 => true [simplification]
  rule isLen(CS:IntSeq) +Int 3 <Int 3 => false [simplification]

  // Function calls allocate a fresh scope location.  The reference semantics
  // intentionally leaves symbolic Map update forms unnormalized; this lemma
  // exposes a freshness-guarded update as the equivalent map binding so the
  // ordinary parameter and lookup rules can match it.
  rule BASE:Map [ N:Int <- S:Scope ] => (N |-> S) BASE
    requires notBool N in_keys(BASE)
    [simplification]
endmodule
