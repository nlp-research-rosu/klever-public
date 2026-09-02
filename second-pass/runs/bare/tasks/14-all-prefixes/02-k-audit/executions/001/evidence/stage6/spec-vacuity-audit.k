requires "verified-lemma.k"

module SPEC-VACUITY-AUDIT
  imports VERIFIED-LEMMA

  // Deliberately false: every call is claimed to return the empty list.
  // S = "a" satisfies the precondition but Python and the K semantics return ["a"].
  claim <mpy>
          <k> Run(solutionProgram,
                   Call(Name("all_prefixes"), Str(S)))
            => listVal(vnil) </k>
          <env> emptyEnv => emptyEnv </env>
          <functions> emptyFEnv => ?_:FEnv </functions>
        </mpy>
    requires 0 <=Int lengthString(S)
endmodule
