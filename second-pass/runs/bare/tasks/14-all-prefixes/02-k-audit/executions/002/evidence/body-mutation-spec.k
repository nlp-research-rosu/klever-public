requires "body-mutation-verification.k"

module BODY-MUTATION-SPEC
  imports BODY-MUTATION-VERIFICATION

  claim <mpy>
          <k> Run(mutatedProgram,
                   Call(Name("all_prefixes"), Str("a")))
            => listVal(allPrefixes("a")) </k>
          <env> emptyEnv => emptyEnv </env>
          <functions> emptyFEnv => ?_:FEnv </functions>
        </mpy>
endmodule
