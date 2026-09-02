requires "candidate/verification.k"

module TOTALITY-WITNESS
  imports MPY-VERIFICATION

  // False for Python: indexing the empty list raises IndexError rather than
  // returning some integer.  The candidate's over-broad [total] declaration
  // for first nevertheless allows this existential result claim to close.
  claim
    <k>
      eval(
        Subscript(Name("l"), Int(0)),
        "l" |-> pyList(.ISeq))
      => pyInt(?I:Int)
    </k>
    <program> _P:Program </program>
    <env> _RHO:Map </env>
endmodule
