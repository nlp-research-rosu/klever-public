requires "verification-base.k"

module AUDITOR-GROUND-SUMMARY-SPEC
  imports VERIFICATION-BASE

  claim [empty]:
    <k> belowFrom(0, .ValSeq) => false </k>

  claim [all-positive]:
    <k> belowFrom(0, vCons(1, vCons(2, vCons(3, .ValSeq)))) => false </k>

  claim [documented-deficit]:
    <k> belowFrom(0, vCons(1, vCons(2, vCons(-4, vCons(5, .ValSeq))))) => true </k>

  claim [zero-boundary-then-deficit]:
    <k> belowFrom(0, vCons(10, vCons(-10, vCons(-1, .ValSeq)))) => true </k>
endmodule
