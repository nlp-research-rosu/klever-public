requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  claim [ground-main-empty]:
    <k> #targetCall(mainCall, ref(0), 0, 0) => 0 </k>
    <heap> 0 |-> list(.ValSeq) </heap>

  claim [ground-main-example-seven]:
    <k> #targetCall(mainCall, ref(0), 0, 0) => 1 </k>
    <heap>
      0 |-> list(
        vCons(1, vCons(2, vCons(3, vCons(4,
        vCons(3, vCons(2, vCons(2, .ValSeq))))))))
    </heap>

  claim [ground-main-example-eight]:
    <k> #targetCall(mainCall, ref(0), 0, 0) => 4 </k>
    <heap>
      0 |-> list(
        vCons(1, vCons(2, vCons(3, vCons(5,
        vCons(4, vCons(7, vCons(9, vCons(6, .ValSeq)))))))))
    </heap>

  claim [ground-helper-valid]:
    <k> #targetCall(helperCall, ref(0), 0, 6) => 1 </k>
    <heap>
      0 |-> list(
        vCons(1, vCons(2, vCons(3, vCons(4,
        vCons(3, vCons(2, vCons(2, .ValSeq))))))))
    </heap>
endmodule
