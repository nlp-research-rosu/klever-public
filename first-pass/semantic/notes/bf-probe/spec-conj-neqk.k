requires "verif.k"
module SPEC-CONJ-NEQK imports BF-PROBE
  // original conjunction-fallback form — expected to REPRODUCE the failure
  claim <k> chkConj(P:IntSeq) => true </k>
    requires P =/=K strToCodes("A") andBool P =/=K strToCodes("B") [all-path]
endmodule
