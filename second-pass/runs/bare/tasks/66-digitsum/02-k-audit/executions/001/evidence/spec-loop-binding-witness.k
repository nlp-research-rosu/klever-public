requires "semantic.k"

module SPEC-LOOP-BINDING-WITNESS
  imports SEMANTIC

  // The generated semantics produces 66 because its loop rule does not bind
  // char.  This is false for Python, which produces 65 for input "A".
  claim [semantic-result]:
        <k>
        Module(
          FuncDef("digitSum", Params("s"),
            Assign(Name("total"), Int(0))
            Assign(Name("char"), Str("B"))
            For(Name("char"), Name("s"),
              If(Compare(Str("A"),
                   CmpOp("<=", Name("char")), CmpOp("<=", Str("Z"))),
                 Assign(Name("total"),
                   BinOp("+", Name("total"),
                     Call(Name("ord"), Name("char")))),
                 .Stmts))
            Return(Call(Name("ord"), Name("char")))))
          => .K
          </k>
          <input> "A" => "A" </input>
          <env> .Map => .Map </env>
          <result> noResult => intVal(66) </result>

  // The correct Python result.  This must get stuck under the candidate
  // semantics, exposing the false transition made by loopString.
  claim [python-result]:
        <k>
        Module(
          FuncDef("digitSum", Params("s"),
            Assign(Name("total"), Int(0))
            Assign(Name("char"), Str("B"))
            For(Name("char"), Name("s"),
              If(Compare(Str("A"),
                   CmpOp("<=", Name("char")), CmpOp("<=", Str("Z"))),
                 Assign(Name("total"),
                   BinOp("+", Name("total"),
                     Call(Name("ord"), Name("char")))),
                 .Stmts))
            Return(Call(Name("ord"), Name("char")))))
          => .K
          </k>
          <input> "A" => "A" </input>
          <env> .Map => .Map </env>
          <result> noResult => intVal(65) </result>
endmodule
