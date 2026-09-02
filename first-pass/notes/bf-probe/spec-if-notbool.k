requires "verif.k"
module SPEC-IF-NOTBOOL imports BF-PROBE
  // #if cascade; invalid precond stated with notBool(==K) (mirrors the #branch path-cond atom)
  claim <k> chkIf(P:IntSeq) => true </k>
    requires notBool (P ==K strToCodes("A")) andBool notBool (P ==K strToCodes("B")) [all-path]
endmodule
