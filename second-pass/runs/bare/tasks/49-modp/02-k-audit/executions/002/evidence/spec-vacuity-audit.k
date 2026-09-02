requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports MODP-VERIFICATION

  // Fresh false result obligation. The precondition is satisfied at n=3,p=5,
  // where both Python implementations and fixed K execution return 3, not 4.
  claim <k>
          Module(FuncDef("modp", Params("n", "p"),
            Return(Call(Name("pow"), Int(2), Name("n"), Name("p")))))
        => .K
        </k>
        <n> 3 </n>
        <p> 5 </p>
        <formals> noFormals => formals("n", "p") </formals>
        <result> noResult => result(4) </result>
endmodule
