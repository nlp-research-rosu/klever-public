requires "verif.k"
module SPEC-CONJNB-NOTBOOL imports BF-PROBE
  claim <k> chkConjNB(P:IntSeq) => true </k>
    requires notBool (P ==K strToCodes("A")) andBool notBool (P ==K strToCodes("B")) [all-path]
endmodule
