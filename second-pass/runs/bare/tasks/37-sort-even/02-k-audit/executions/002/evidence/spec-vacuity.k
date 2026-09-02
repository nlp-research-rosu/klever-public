requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for the satisfying input []: the returned list has size zero,
  // not one. This mutates a result-bearing obligation only.
  claim <k>
          run(pyList(.List))
        => pyList(?RESULT:List)
        ...
        </k>
        <program> solutionProgram() </program>
    ensures size(?RESULT) ==Int 1
    [label(false-empty-length)]
endmodule
