requires "verification.k"

module SPEC-AUDIT
  imports VERIFICATION

  // The loop invariant: E and O are the counts accumulated so far, while N
  // is the nonnegative suffix of digits still to consume.
  claim [loop-invariant]:
        <mpy>
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

  // End-to-end correctness for every mathematical integer input.
  claim [end-to-end]:
        <mpy>
          <k> solutionProgram() => .K </k>
          <env> .Map
              => ("num" |-> intVal(0)
                  "even" |-> intVal(evenDigits(absNum(N)))
                  "odd" |-> intVal(oddDigits(absNum(N)))) </env>
          <input> N </input>
          <result> noResult => expected(N) </result>
        </mpy>
endmodule
