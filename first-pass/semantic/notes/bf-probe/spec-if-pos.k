requires "verif.k"
module SPEC-IF-POS imports BF-PROBE
  // positive sanity: the cascade DOES reduce a matched atom (expect #Top)
  claim <k> chkIfPos(P:IntSeq) => true </k>
    requires P ==K strToCodes("A") [all-path]
endmodule
