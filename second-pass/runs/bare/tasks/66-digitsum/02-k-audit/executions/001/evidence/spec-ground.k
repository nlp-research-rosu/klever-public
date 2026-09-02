requires "semantic.k"

module SPEC-GROUND
  imports SEMANTIC
  imports DIGIT-SUM-VERIFICATION

  claim [entry-AZ]:
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
          <input> "AZ" => "AZ" </input>
          <env> .Map => .Map </env>
          <result> noResult => intVal(155) </result>

  claim [loop-A-at]:
        <k>
            loopString("char", "A@",
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
          <input> "" => "" </input>
          <env> "total" |-> intVal(10) => .Map </env>
          <result> noResult => intVal(75) </result>
endmodule
