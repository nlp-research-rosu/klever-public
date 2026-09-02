requires "verification.k"

module SPEC
  imports VERIFICATION

  // This is the literal tree in solution.mpy; the claim checks that the
  // shared proof abbreviation expands to exactly that emitted program.
  claim [emitted-tree-is-shared-tree]:
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
            Assign(Name("power"), BinOp("*", Name("power"), Name("n"))))
          Return(Compare(Name("power"), CmpOp("==", Name("x"))))))
      => solutionProgram
    </k>
    <env> .Map </env>
    <result> noResult </result>
    <x> _X </x>
    <n> _N </n>

  // These four path claims partition all integer inputs.  The final active
  // path reaches the source configuration of loop-correct with P = N.
  claim [returns-on-one]:
    <k> solutionProgram => .K </k>
    <env> .Map => ("x" |-> 1) ("n" |-> N) </env>
    <result> noResult => simplePowerSpec(1, N) </result>
    <x> 1 </x>
    <n> N </n>

  claim [rejects-below-one]:
    <k> solutionProgram => .K </k>
    <env> .Map => ("x" |-> X) ("n" |-> N) </env>
    <result> noResult => simplePowerSpec(X, N) </result>
    <x> X </x>
    <n> N </n>
    requires X <Int 1

  claim [rejects-small-base]:
    <k> solutionProgram => .K </k>
    <env> .Map => ("x" |-> X) ("n" |-> N) </env>
    <result> noResult => simplePowerSpec(X, N) </result>
    <x> X </x>
    <n> N </n>
    requires 1 <Int X andBool N <Int 2

  claim [active-path-enters-loop]:
    <k>
      solutionProgram
      => While(Compare(Name("power"), CmpOp("<", Name("x"))),
           Assign(Name("power"), BinOp("*", Name("power"), Name("n"))))
         ~> exec(Return(Compare(Name("power"), CmpOp("==", Name("x")))))
    </k>
    <env>
      .Map => ("x" |-> X) ("n" |-> N) ("power" |-> N)
    </env>
    <result> noResult </result>
    <x> X </x>
    <n> N </n>
    requires 1 <Int X andBool 2 <=Int N

  claim [loop-correct]:
    <k>
      While(Compare(Name("power"), CmpOp("<", Name("x"))),
        Assign(Name("power"), BinOp("*", Name("power"), Name("n"))))
      ~> exec(Return(Compare(Name("power"), CmpOp("==", Name("x")))))
      => .K
    </k>
    <env>
      ("x" |-> X) ("n" |-> N) ("power" |-> P)
      => ("x" |-> X) ("n" |-> N)
         ("power" |-> powerCeiling(P, X, N))
    </env>
    <result> noResult => powerCeiling(P, X, N) ==Int X </result>
    <x> X </x>
    <n> N </n>
    requires 1 <Int X andBool 2 <=Int N andBool 0 <Int P

endmodule
