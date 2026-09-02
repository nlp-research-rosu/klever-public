requires "verification.k"

module STAGE4-ROWS-EVAL-SPEC
  imports VERIFICATION

  claim [ground-rows-append]:
    <k> rowsAppend(
      .ValSeq,
      vCons(
        list(vCons(2, vCons(1, vCons(2, .ValSeq)))),
        vCons(
          list(vCons(2, .ValSeq)),
          vCons(
            list(vCons(1, vCons(2, vCons(1, vCons(2, .ValSeq))))),
            .ValSeq))),
      2,
      0)
    =>
    vCons(
      tuple(vCons(0, vCons(0, .ValSeq))),
      vCons(
        tuple(vCons(0, vCons(2, .ValSeq))),
        vCons(
          tuple(vCons(1, vCons(0, .ValSeq))),
          vCons(
            tuple(vCons(2, vCons(1, .ValSeq))),
            vCons(tuple(vCons(2, vCons(3, .ValSeq))), .ValSeq))))) </k>
endmodule
