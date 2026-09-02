requires "verification.k"

module TOTALITY-GAP-PROBE
  imports VERIFICATION

  // sumIntVS is declared total over ValSeq but has no non-Int-head equation.
  // This probe checks that the backend does not fabricate a numeric result.
  claim
    <k> sumIntVS(vCons(true, .ValSeq)) => 0 </k>
endmodule
