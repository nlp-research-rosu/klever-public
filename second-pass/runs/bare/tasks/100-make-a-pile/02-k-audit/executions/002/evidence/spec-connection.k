requires "semantic.k"

module CONNECTION-SPEC
  imports MPY

  // Candidate bridge-free obligation: execute the real concrete loop from an
  // arbitrary invariant state to the claimed final configuration.
  claim [loop-connection]:
    <mpy>
      <k>
        While(Compare(Name("i"), CmpOp(">=", Int(0))),
          Assign(Name("result"),
            BinOp("+",
              ListExpr(BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))),
              Name("result")))
          Assign(Name("i"), BinOp("-", Name("i"), Int(1))))
        ~> exec(Return(Name("result")))
      =>
        .K
      </k>
      <n> N </n>
      <env>
        "i" |-> VInt(I)
        "n" |-> VInt(N)
        "result" |-> VList(pileFrom(N, I +Int 1))
      =>
        "i" |-> VInt(-1)
        "n" |-> VInt(N)
        "result" |-> VList(pileFrom(N, 0))
      </env>
      <result> VNone => VList(pileFrom(N, 0)) </result>
    </mpy>
    requires N >Int 0 andBool I >=Int -1 andBool I <Int N
endmodule
