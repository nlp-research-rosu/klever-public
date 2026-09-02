requires "verified-lemma.k"

module SPEC
  imports VERIFIED-LEMMA

  claim <mpy>
          <k> Run(solutionProgram,
                   Call(Name("all_prefixes"), Str(S)))
            => listVal(allPrefixes(S)) </k>
          <env> emptyEnv => emptyEnv </env>
          <functions> emptyFEnv => ?_:FEnv </functions>
        </mpy>
    requires 0 <=Int lengthString(S)
endmodule
