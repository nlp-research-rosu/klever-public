requires "semantic.k"

module SPEC-BODY-MUTATION
  imports SEMANTIC
  imports DIGIT-SUM-VERIFICATION

  // Material mutation of the actual constructor term: initialize total to 1.
  claim <k>
      Module(
        FuncDef("digitSum", Params("s"),
          Assign(Name("total"), Int(1))
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

  claim <k>
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
