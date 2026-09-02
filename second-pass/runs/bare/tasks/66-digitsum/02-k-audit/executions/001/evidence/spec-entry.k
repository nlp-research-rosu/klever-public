requires "semantic.k"

module SPEC-ENTRY
  imports SEMANTIC
  imports DIGIT-SUM-VERIFICATION

  claim [entry]:
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
          <result> noResult => intVal(upperAsciiSum(S)) </result>
endmodule
