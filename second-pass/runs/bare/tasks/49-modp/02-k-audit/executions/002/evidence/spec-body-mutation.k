requires "verification.k"

module AUDIT-SPEC-BODY-MUTATION
  imports MODP-VERIFICATION

  // Materially mutates the executed submitted body: base 2 becomes base 3.
  // At the satisfying ground witness n=1,p=5, the original result is 2 while
  // this body returns 3.
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
