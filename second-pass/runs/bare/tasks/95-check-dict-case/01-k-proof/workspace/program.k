requires "semantic.k"

module SOLUTION-PROGRAM
  imports MPY-SYNTAX

  syntax PyStmt ::= "solutionProgram" [function]
  rule solutionProgram => Module(
    FuncDef("check_dict_case", Params("dict"),
      If(UnaryOp("not", Name("dict")),
        Return(Bool(false)),
        )
      Assign(Name("lower"), Bool(true))
      Assign(Name("upper"), Bool(true))
      For(Name("key"), Name("dict"),
        If(UnaryOp("not", Call(Name("isinstance"), Name("key"), Name("str"))),
          Return(Bool(false)),
          )
        If(UnaryOp("not", Call(Attribute(Name("key"), "islower"), )),
          Assign(Name("lower"), Bool(false)),
          )
        If(UnaryOp("not", Call(Attribute(Name("key"), "isupper"), )),
          Assign(Name("upper"), Bool(false)),
          ))
      Return(BoolOp("or", Name("lower"), Name("upper")))))
endmodule
