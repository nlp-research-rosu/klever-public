requires "verification.k"

module SPEC
  imports VERIFICATION

  // The example from the HumanEval prompt.
  claim
    <python>
      <k> verify(solutionProgram, vlist(1, 2, 3, 4, 5, .Rats))
           => done(vlist(0, 1 /Rat 4, 1 /Rat 2, 3 /Rat 4, 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>

  // Negative values, a non-integral result, and a repeated maximum.
  claim
    <python>
      <k> verify(solutionProgram, vlist(-5, 0, 5, 5, .Rats))
           => done(vlist(0, 1 /Rat 2, 1, 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>

  // For every increasing two-point input, the endpoints become exactly 0, 1.
  claim
    <python>
      <k> verify(solutionProgram, vlist(A, B, .Rats))
           => done(vlist(0, 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B

  // A symbolic three-point proof: endpoints are 0 and 1 and the middle value
  // is precisely the contract's affine transform.
  claim
    <python>
      <k> verify(solutionProgram, vlist(A, B, C, .Rats))
           => done(vlist(0, (B -Rat A) /Rat (C -Rat A), 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B andBool B <Rat C andBool A <Rat C

  // The operational result also agrees directly with the independent
  // mathematical reference function in verification.k.
  claim
    <python>
      <k> verify(solutionProgram, vlist(A, B, C, .Rats))
           => done(rescaleSpec(vlist(A, B, C, .Rats)))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B andBool B <Rat C andBool A <Rat C andBool A =/=Rat C

  // Ordering is not assumed by the implementation: the same symbolic values
  // in descending order are transformed pointwise and retain their positions.
  claim
    <python>
      <k> verify(solutionProgram, vlist(C, B, A, .Rats))
           => done(vlist(1, (B -Rat A) /Rat (C -Rat A), 0, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B andBool B <Rat C andBool A <Rat C

  // Repeated extrema remain repeated extrema after rescaling.
  claim
    <python>
      <k> verify(solutionProgram, vlist(A, A, B, B, .Rats))
           => done(vlist(0, 0, 1, 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B
endmodule
