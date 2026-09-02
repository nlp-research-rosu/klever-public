requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION

  claim <mpy>
          <k>
            loop(
              Compare(Name("i"),
                CmpOp("<=", Call(Name("len"), Name("string")))),
              Expr(Call(Attribute(Name("result"), "append"),
                Subscript(Name("string"),
                  Slice(NoBound, Name("i"), NoBound))))
              Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
            ~> exec(Return(Name("result")))
            ~> restoreEnv(OLD)
            => listVal(allPrefixes(S))
          </k>
          <env>
            bind("string", strVal(S),
              bind("result", listVal(pacc(S, N)),
                bind("i", intVal(I), emptyEnv)))
            => OLD
          </env>
          <functions> _FUNS </functions>
        </mpy>
    requires 0 <=Int lengthString(S)
     andBool 0 <=Int N
     andBool N <=Int lengthString(S)
     andBool I ==Int N +Int 1
endmodule
