requires "reference-semantics/semantics/syntax.k"

module SOLUTION-MODULE-SYNTAX
  imports MPY-SYNTAX
  syntax Module ::= "solutionModule" [function, total]
endmodule

module SOLUTION-MODULE
  imports SOLUTION-MODULE-SYNTAX
  rule solutionModule
    => Module(
         FuncDef("intersection", Params("interval1", "interval2"),
           Assign(Name("start"), Subscript(Name("interval1"), Int(0)))
           If(Compare(
             Subscript(Name("interval2"), Int(0)),
             CmpOp(">", Name("start"))),
             Assign(Name("start"), Subscript(Name("interval2"), Int(0))),
             .Stmts)
           Assign(Name("end"), Subscript(Name("interval1"), Int(1)))
           If(Compare(
             Subscript(Name("interval2"), Int(1)),
             CmpOp("<", Name("end"))),
             Assign(Name("end"), Subscript(Name("interval2"), Int(1))),
             .Stmts)
           Assign(Name("length"), BinOp("-", Name("end"), Name("start")))
           If(Compare(Name("length"), CmpOp("<", Int(2))),
             Return(Str("NO")),
             .Stmts)
           Assign(Name("divisor"), Int(2))
           Assign(Name("has_divisor"), Bool(false))
           While(Compare(Name("divisor"), CmpOp("<", Name("length"))),
             If(Compare(
               BinOp("%", Name("length"), Name("divisor")),
               CmpOp("==", Int(0))),
               Assign(Name("has_divisor"), Bool(true)),
               .Stmts)
             Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
           If(Name("has_divisor"),
             Return(Str("NO")),
             .Stmts)
           Return(Str("NO"))))
endmodule
