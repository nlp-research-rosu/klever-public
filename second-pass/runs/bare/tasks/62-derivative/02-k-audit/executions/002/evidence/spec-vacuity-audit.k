requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Reviewer mutation: the real entry program is unchanged, but the expected
  // result incorrectly starts degrees at two. Witness: input [3, 5] returns
  // [5], while this postcondition demands [10].
  claim
    <mpy>
      <k>
        #run(solutionProgram,
          ListV((_C0:Value, CS:Values)))
        => ListV(#differentiate(2, CS))
      </k>
    </mpy>
    [label(false-degree-start), depends(helper-correct)]
endmodule
