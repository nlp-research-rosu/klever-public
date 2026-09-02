requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports MODP-VERIFICATION

  // Fresh off-by-one mutation of the result-constraining general obligation.
  // The precondition is satisfiable, for example at N = 3 and P = 5, where
  // execution returns 3 but this destination requires 4.
  claim <k>
          Module(FuncDef("modp", Params("n", "p"),
            Return(Call(Name("pow"), Int(2), Name("n"), Name("p")))))
        => .K
        </k>
        <n> N </n>
        <p> P </p>
        <formals> noFormals => formals("n", "p") </formals>
        <result>
          noResult => result(expectedModp(N, P) +Int 1)
        </result>
    requires (N >=Int 0) andBool (P >Int 0)
endmodule
