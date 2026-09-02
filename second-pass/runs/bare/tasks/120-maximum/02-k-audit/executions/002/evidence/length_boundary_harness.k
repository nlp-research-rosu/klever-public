requires "semantic.k"

module LENGTH-BOUNDARY-HARNESS
  imports MAXIMUM

  syntax Module ::= "Boundary1000"
  syntax List ::= "zeros" "(" Int ")" [function]

  rule zeros(0) => .List
  rule zeros(N:Int) => ListItem(0) zeros(N -Int 1)
    requires N >Int 0

  rule
    <k> Boundary1000 ~> boot
      => Module(
           FuncDef("maximum", Params("arr", "k"),
             Return(
               Subscript(
                 Call(Name("sorted"), Name("arr")),
                 Slice(
                   BinOp("-", Call(Name("len"), Name("arr")), Name("k")),
                   NoBound,
                   NoBound)))))
         ~> boot
         ...
    </k>
    <args> .List => ListItem(listVal(zeros(1000))) ListItem(intVal(3)) </args>
endmodule
