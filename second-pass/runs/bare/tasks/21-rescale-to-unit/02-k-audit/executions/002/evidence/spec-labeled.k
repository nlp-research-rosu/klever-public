// Reviewer copy of candidate spec.k with labels added and no claim-body changes.
requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [claim-01]:
    <python>
      <k> verify(solutionProgram, vlist(1, 2, 3, 4, 5, .Rats))
           => done(vlist(0, 1 /Rat 4, 1 /Rat 2, 3 /Rat 4, 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>

  claim [claim-02]:
    <python>
      <k> verify(solutionProgram, vlist(-5, 0, 5, 5, .Rats))
           => done(vlist(0, 1 /Rat 2, 1, 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>

  claim [claim-03]:
    <python>
      <k> verify(solutionProgram, vlist(A, B, .Rats))
           => done(vlist(0, 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B

  claim [claim-04]:
    <python>
      <k> verify(solutionProgram, vlist(A, B, C, .Rats))
           => done(vlist(0, (B -Rat A) /Rat (C -Rat A), 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B andBool B <Rat C andBool A <Rat C

  claim [claim-05]:
    <python>
      <k> verify(solutionProgram, vlist(A, B, C, .Rats))
           => done(rescaleSpec(vlist(A, B, C, .Rats)))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B andBool B <Rat C andBool A <Rat C andBool A =/=Rat C

  claim [claim-06]:
    <python>
      <k> verify(solutionProgram, vlist(C, B, A, .Rats))
           => done(vlist(1, (B -Rat A) /Rat (C -Rat A), 0, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
    requires A <Rat B andBool B <Rat C andBool A <Rat C

  claim [claim-07]:
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
