requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: empty lists are monotonic, so requiring false is
  // a deliberately false result obligation for a realizable input.
  claim <k>
          #run(solutionProgram, listVal(nil))
        => boolVal(false)
        </k>
endmodule
