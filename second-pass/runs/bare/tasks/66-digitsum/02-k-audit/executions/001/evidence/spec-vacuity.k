requires "semantic.k"

module SPEC-VACUITY
  imports SEMANTIC
  imports DIGIT-SUM-VERIFICATION

  // Fresh false mutation: the real result is upperAsciiSum(S), not that value
  // plus one.  S = "" is a satisfying witness with actual 0 and demanded 1.
  claim [mutated-entry]:
        <k>
        Module(
          FuncDef("digitSum", Params("s"),
            Assign(Name("total"), Int(0))
            For(Name("char"), Name("s"),
              If(Compare(Str("A"),
                   CmpOp("<=", Name("char")), CmpOp("<=", Str("Z"))),
                 Assign(Name("total"),
                   BinOp("+", Name("total"),
                     Call(Name("ord"), Name("char")))),
                 .Stmts))
            Return(Name("total"))))
          => .K
          </k>
          <input> S:String => S:String </input>
          <env> .Map => .Map </env>
          <result>
            noResult => intVal(upperAsciiSum(S) +Int 1)
          </result>

  // Exact original invariant, already independently reconstructed as #Top.
  // It is marked trusted only in the mutation command so the failure isolates
  // the changed entry result rather than removal of its supporting lemma.
  claim [loop]:
        <k>
            loopString("char", S:String,
              If(Compare(Str("A"),
                   CmpOp("<=", Name("char")), CmpOp("<=", Str("Z"))),
                 Assign(Name("total"),
                   BinOp("+", Name("total"),
                     Call(Name("ord"), Name("char")))),
                 .Stmts)
              .Stmts)
            ~> execute(Return(Name("total")) .Stmts)
            ~> .K
            => .K
          </k>
          <input> INPUT:String => INPUT:String </input>
          <env>
            ("total" |-> intVal(A:Int)) FRAME:Map
            => .Map
          </env>
          <result>
            noResult => intVal(A +Int upperAsciiSum(S))
          </result>
      requires notBool ("total" in_keys(FRAME))
endmodule
