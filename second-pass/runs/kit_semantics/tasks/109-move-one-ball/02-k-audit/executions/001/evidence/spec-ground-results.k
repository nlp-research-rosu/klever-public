requires "verification.k"

module SPEC-GROUND-RESULTS
  imports VERIFICATION

  claim [ground-empty]:
    <k> moveSpec(.ValSeq) => true ... </k>

  claim [ground-prompt-true]:
    <k> moveSpec(vCons(3, vCons(4, vCons(5, vCons(1, vCons(2, .ValSeq))))))
      => true ... </k>

  claim [ground-prompt-false]:
    <k> moveSpec(vCons(3, vCons(5, vCons(4, vCons(1, vCons(2, .ValSeq))))))
      => false ... </k>
endmodule
