requires "verified-lemma.k"

module SPEC-VACUITY
  imports VERIFIED-LEMMA

  // Deliberately false: all_prefixes("a") returns ["a"], not [].
  claim <mpy>
          <k> Run(solutionProgram,
                   Call(Name("all_prefixes"), Str("a")))
            => listVal(vnil) </k>
          <env> emptyEnv => emptyEnv </env>
          <functions> emptyFEnv => ?_:FEnv </functions>
        </mpy>
endmodule
