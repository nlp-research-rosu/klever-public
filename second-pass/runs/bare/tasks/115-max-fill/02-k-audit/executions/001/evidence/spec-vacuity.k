requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [water]:
    <max-fill>
      <k>
        invoke("_water_in", arg(rowVal(ROW), noArgs)) ~> CONT
        => intVal(water(ROW)) ~> CONT
      </k>
      <args> ARGS </args>
      <functions> solutionFunctions </functions>
      <env> ENV </env>
      <result> RES </result>
    </max-fill>

  claim [buckets]:
    <max-fill>
      <k>
        invoke(
          "_buckets_for",
          arg(gridVal(GRID), arg(intVal(C), noArgs))) ~> CONT
        => intVal(requiredBuckets(GRID, C)) ~> CONT
      </k>
      <args> ARGS </args>
      <functions> solutionFunctions </functions>
      <env> ENV </env>
      <result> RES </result>
    </max-fill>
    requires C >Int 0

  // Fresh reviewer mutation: the real result is forced to be one too large.
  claim [entry-off-by-one]:
    <max-fill>
      <k> solutionProgram => .K </k>
      <args> gridVal(GRID), intVal(C) </args>
      <functions> .Map => solutionFunctions </functions>
      <env> .Map </env>
      <result>
        noneVal => intVal(requiredBuckets(GRID, C) +Int 1)
      </result>
    </max-fill>
    requires C >Int 0
endmodule
