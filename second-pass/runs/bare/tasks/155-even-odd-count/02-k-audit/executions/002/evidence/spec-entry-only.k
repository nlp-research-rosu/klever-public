requires "verification.k"

module SPEC-ENTRY-ONLY
  imports VERIFICATION

  claim <mpy>
          <k> solutionProgram() => .K </k>
          <env> .Map
              => ("num" |-> intVal(0)
                  "even" |-> intVal(evenDigits(absNum(N)))
                  "odd" |-> intVal(oddDigits(absNum(N)))) </env>
          <input> N </input>
          <result> noResult => expected(N) </result>
        </mpy>
endmodule
