requires "verification.k"

module MODP-SPEC
  imports MODP-VERIFICATION

  // General functional correctness on the task's natural modular-arithmetic
  // domain: every nonnegative exponent and every positive modulus.
  claim <k>
          Module(FuncDef("modp", Params("n", "p"),
            Return(Call(Name("pow"), Int(2), Name("n"), Name("p")))))
        => .K
        </k>
        <n> N </n>
        <p> P </p>
        <formals> noFormals => formals("n", "p") </formals>
        <result> noResult => result(expectedModp(N, P)) </result>
    requires (N >=Int 0) andBool (P >Int 0)

  // The five examples from prompt.py are also independent ground claims.
  claim <k>
          Module(FuncDef("modp", Params("n", "p"),
            Return(Call(Name("pow"), Int(2), Name("n"), Name("p")))))
        => .K
        </k>
        <n> 3 </n>
        <p> 5 </p>
        <formals> noFormals => formals("n", "p") </formals>
        <result> noResult => result(3) </result>

  claim <k>
          Module(FuncDef("modp", Params("n", "p"),
            Return(Call(Name("pow"), Int(2), Name("n"), Name("p")))))
        => .K
        </k>
        <n> 1101 </n>
        <p> 101 </p>
        <formals> noFormals => formals("n", "p") </formals>
        <result> noResult => result(2) </result>

  claim <k>
          Module(FuncDef("modp", Params("n", "p"),
            Return(Call(Name("pow"), Int(2), Name("n"), Name("p")))))
        => .K
        </k>
        <n> 0 </n>
        <p> 101 </p>
        <formals> noFormals => formals("n", "p") </formals>
        <result> noResult => result(1) </result>

  claim <k>
          Module(FuncDef("modp", Params("n", "p"),
            Return(Call(Name("pow"), Int(2), Name("n"), Name("p")))))
        => .K
        </k>
        <n> 3 </n>
        <p> 11 </p>
        <formals> noFormals => formals("n", "p") </formals>
        <result> noResult => result(8) </result>

  claim <k>
          Module(FuncDef("modp", Params("n", "p"),
            Return(Call(Name("pow"), Int(2), Name("n"), Name("p")))))
        => .K
        </k>
        <n> 100 </n>
        <p> 101 </p>
        <formals> noFormals => formals("n", "p") </formals>
        <result> noResult => result(1) </result>
endmodule
