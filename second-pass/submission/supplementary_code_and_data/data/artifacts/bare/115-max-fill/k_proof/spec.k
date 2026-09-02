requires "verification.k"

module SPEC
  imports VERIFICATION

  // Lemma 1: the translated recursive row helper computes mathematical sum.
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

  // Lemma 2: the translated grid helper computes the sum of per-row ceilings.
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

  // End-to-end theorem about the entry point in the actual translated module.
  claim
    <max-fill>
      <k> solutionProgram => .K </k>
      <args> gridVal(GRID), intVal(C) </args>
      <functions> .Map => solutionFunctions </functions>
      <env> .Map </env>
      <result>
        noneVal => intVal(requiredBuckets(GRID, C))
      </result>
    </max-fill>
    requires C >Int 0
endmodule
