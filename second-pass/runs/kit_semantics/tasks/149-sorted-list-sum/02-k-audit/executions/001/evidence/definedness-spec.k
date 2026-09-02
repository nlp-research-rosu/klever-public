requires "reference-semantics/semantics.k"

module DEFINEDNESS-SPEC
  imports MPY

  // Reviewer check of the candidate's only derived simplification, using the
  // fixed supplied semantics without importing verification.k.
  claim [string-length-computes]:
    <k> seqLen(str(CS:IntSeq)) => isLen(CS) </k>
endmodule
