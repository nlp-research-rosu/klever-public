requires "reference-semantics/semantics.k"

module CLASSIFIER-CONNECTION
  imports MPY

  claim [classifier-connection]:
    <k>
      isIntV(V:Val)
      =>
      isInt(V) orBool isBool(V)
    </k>
endmodule
