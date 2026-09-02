requires "verification.k"

module SPEC-LOOP-ONLY
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
endmodule
