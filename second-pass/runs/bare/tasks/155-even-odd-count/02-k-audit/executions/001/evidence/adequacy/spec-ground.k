requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  // N=12, E=0, O=0 satisfies the loop claim's N >=Int 0 precondition.
  claim [loop-ground]:
        <mpy>
          <k> loop(numPositive(), digitBody()) ~> exec(returnCounts())
              => .K </k>
          <env> ("num" |-> intVal(12)
                 "even" |-> intVal(0)
                 "odd" |-> intVal(0))
              => ("num" |-> intVal(0)
                  "even" |-> intVal(1)
                  "odd" |-> intVal(1)) </env>
          <input> -12 </input>
          <result> noResult
                => pairVal(intVal(1), intVal(1)) </result>
        </mpy>

  // The entry claim has no requires clause, so N=-12 is satisfying.
  claim [entry-ground-negative]:
        <mpy>
          <k> solutionProgram() => .K </k>
          <env> .Map
              => ("num" |-> intVal(0)
                  "even" |-> intVal(1)
                  "odd" |-> intVal(1)) </env>
          <input> -12 </input>
          <result> noResult => pairVal(intVal(1), intVal(1)) </result>
        </mpy>

  // N=0 also satisfies the unconditional entry claim and exposes the intent gap.
  claim [entry-ground-zero]:
        <mpy>
          <k> solutionProgram() => .K </k>
          <env> .Map
              => ("num" |-> intVal(0)
                  "even" |-> intVal(0)
                  "odd" |-> intVal(0)) </env>
          <input> 0 </input>
          <result> noResult => pairVal(intVal(0), intVal(0)) </result>
        </mpy>
endmodule
