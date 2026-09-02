requires "post-eval.k"

module POST-EVAL-SPEC
  imports POST-EVAL

  claim
    <post>
      buildVS(
        sortVS(vCons(-3, vCons(5, .ValSeq))),
        1,
        2,
        1)
      => vCons(5, .ValSeq)
    </post>

  claim
    <post>
      buildVS(
        sortVS(vCons(-3, vCons(5, .ValSeq))),
        0,
        2,
        1)
      => vCons(-3, vCons(5, .ValSeq))
    </post>
endmodule
