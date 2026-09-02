requires "reference-semantics/semantics.k"

module LEMMA-SPEC
  imports MPY

  // Bridge-free universal derivation of verification.k's one-character
  // lexicographic simplification.
  claim [single-char-str-lt-less]:
    <k>
      strLt(
        iCons(C:Int, .IntSeq),
        iCons(D:Int, .IntSeq))
      => true
    </k>
    requires C <Int D

  claim [single-char-str-lt-greater]:
    <k>
      strLt(
        iCons(C:Int, .IntSeq),
        iCons(D:Int, .IntSeq))
      => false
    </k>
    requires C >Int D

  claim [single-char-str-lt-equal]:
    <k>
      strLt(
        iCons(C:Int, .IntSeq),
        iCons(D:Int, .IntSeq))
      => false
    </k>
    requires C ==Int D
endmodule
