requires "verification.k"

module XOR-SPEC-VACUITY-AUDIT
  imports XOR-VERIFICATION

  // False result mutation: string_xor("0", "1") is "1", not "0".
  // The executed program term and input state are unchanged; only the
  // result-constraining destination is mutated.
  claim [false-zero-result]:
    <k> solutionProgram => returned(str(cons(false, empty))) ... </k>
    <args>
      Args(str(segment(1, seed(0))), str(segment(1, seed(1))))
    </args>
endmodule
