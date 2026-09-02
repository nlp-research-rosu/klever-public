requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  claim <mpy>
          <k> loop(numPositive(), digitBody()) ~> exec(returnCounts())
              => .K </k>
          <env> ("num" |-> intVal(N)
                 "even" |-> intVal(E)
                 "odd" |-> intVal(O))
              => ("num" |-> intVal(0)
                  "even" |-> intVal(evenFrom(E, N))
                  "odd" |-> intVal(oddFrom(O, N))) </env>
          <input> _INPUT </input>
          <result> noResult
                => pairVal(intVal(evenFrom(E, N)),
                           intVal(oddFrom(O, N))) </result>
        </mpy>
    requires N >=Int 0

  // Fresh audit mutation: demand one extra even digit in the returned pair.
  // N = 12 is a satisfying witness: execution returns (1,1), not (2,1).
  claim <mpy>
          <k> solutionProgram() => .K </k>
          <env> .Map
              => ("num" |-> intVal(0)
                  "even" |-> intVal(evenDigits(absNum(N)))
                  "odd" |-> intVal(oddDigits(absNum(N)))) </env>
          <input> N </input>
          <result> noResult
                => pairVal(
                     intVal(evenDigits(absNum(N)) +Int 1),
                     intVal(oddDigits(absNum(N)))) </result>
        </mpy>
endmodule
