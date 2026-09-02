requires "verification.k"

module AUDIT-BODY-MUTATION
  imports MODP-VERIFICATION

  // Body sensitivity witness: the base is changed from 2 to 3.
  // At n = 1 and p = 5 the mutated execution returns 3, not 2.
  claim <k>
          Module(FuncDef("modp", Params("n", "p"),
            Return(Call(Name("pow"), Int(3), Name("n"), Name("p")))))
        => .K
        </k>
        <n> 1 </n>
        <p> 5 </p>
        <formals> noFormals => formals("n", "p") </formals>
        <result> noResult => result(2) </result>
endmodule
