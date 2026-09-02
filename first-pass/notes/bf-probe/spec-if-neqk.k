requires "verif.k"
module SPEC-IF-NEQK imports BF-PROBE
  // #if cascade; invalid precond stated with =/=K (mirrors idxOf fallback's atom form)
  claim <k> chkIf(P:IntSeq) => true </k>
    requires P =/=K strToCodes("A") andBool P =/=K strToCodes("B") [all-path]
endmodule
