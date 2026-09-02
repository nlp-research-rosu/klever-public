requires "verification.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // Deliberately mutate the real loop multiplier from n to the integer 3.
  // This keeps every mutated construct inside the modeled language.
  // The original active-path target must no longer be reachable.
  claim [mutated-body-does-not-reach-original-loop]:
    <k>
      Module(
        FuncDef("is_simple_power", Params("x", "n"),
          If(Compare(Name("x"), CmpOp("==", Int(1))),
            Return(Bool(true)),
            .Stmts)
          If(Compare(Name("x"), CmpOp("<", Int(1))),
            Return(Bool(false)),
            .Stmts)
          If(Compare(Name("n"), CmpOp("<", Int(2))),
            Return(Bool(false)),
            .Stmts)
          Assign(Name("power"), Name("n"))
          While(Compare(Name("power"), CmpOp("<", Name("x"))),
            Assign(Name("power"), BinOp("*", Name("power"), Int(3))))
          Return(Compare(Name("power"), CmpOp("==", Name("x"))))))
      => While(Compare(Name("power"), CmpOp("<", Name("x"))),
           Assign(Name("power"), BinOp("*", Name("power"), Name("n"))))
         ~> exec(Return(Compare(Name("power"), CmpOp("==", Name("x")))))
    </k>
    <env> .Map => ("x" |-> 8) ("n" |-> 2) ("power" |-> 2) </env>
    <result> noResult </result>
    <x> 8 </x>
    <n> 2 </n>

endmodule
