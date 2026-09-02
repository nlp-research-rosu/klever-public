requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // This constant is deliberately the exact constructor tree generated in
  // solution.mpy.  Specs execute it through SEMANTIC rather than replacing
  // the program with a mathematical shortcut.
  syntax Module ::= "roundedAvgProgram" [function]
  rule roundedAvgProgram =>
    Module(
      FuncDef("rounded_avg", Params("n", "m"),
        If(Compare(Name("n"), CmpOp(">", Name("m"))),
          Return(UnaryOp("-", Int(1))),
          .Stmts)
        Return(
          Call(
            Name("bin"),
            Call(
              Name("round"),
              BinOp("/", BinOp("+", Name("n"), Name("m")), Int(3)))))))

  // Concrete observer for the abstract binary-string value.  It is kept out
  // of symbolic program execution so an unbounded integer proof does not try
  // to unfold an unbounded number of output bits.
  syntax String ::= "renderBinary" "(" PyVal ")" [function]
                  | "unsignedBits" "(" Int ")" [function]
  rule renderBinary(binVal(I)) => "0b" +String unsignedBits(I)
    requires I >=Int 0
  rule unsignedBits(0) => "0"
  rule unsignedBits(1) => "1"
  rule unsignedBits(I) => unsignedBits(I /Int 2) +String Int2String(I %Int 2)
    requires I >=Int 2
endmodule
