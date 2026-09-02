requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim
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

  claim
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

  // Fresh false mutation: every terminating result is required to be one
  // larger.  An intended-domain witness is GRID=rowVal(0), C=1: execution
  // returns 0, while this destination demands 1.
  claim
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
