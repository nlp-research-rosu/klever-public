requires "semantic.k"

module VERIFICATION
  imports MPY

  // Mathematical contract: sides are positive and one side is the hypotenuse.
  syntax Bool ::= "rightTriangle" "(" Int "," Int "," Int ")" [function, total]
  rule rightTriangle(A, B, C)
       => (A >Int 0)
          andBool (B >Int 0)
          andBool (C >Int 0)
          andBool (((A *Int A) +Int (B *Int B)) ==Int (C *Int C)
                   orBool ((A *Int A) +Int (C *Int C)) ==Int (B *Int B)
                   orBool ((B *Int B) +Int (C *Int C)) ==Int (A *Int A))

  // This is solution.mpy as a K term. Keeping it in the proof definition
  // makes the universal claim execute the translated implementation itself.
  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram
       => Module(
            FuncDef("right_angle_triangle", Params("a", "b", "c"),
              Return(
                BoolOp(
                  "and",
                  Compare(Name("a"), CmpOp(">", Int(0))),
                  Compare(Name("b"), CmpOp(">", Int(0))),
                  Compare(Name("c"), CmpOp(">", Int(0))),
                  BoolOp(
                    "or",
                    Compare(
                      BinOp(
                        "+",
                        BinOp("*", Name("a"), Name("a")),
                        BinOp("*", Name("b"), Name("b"))),
                      CmpOp("==", BinOp("*", Name("c"), Name("c")))),
                    Compare(
                      BinOp(
                        "+",
                        BinOp("*", Name("a"), Name("a")),
                        BinOp("*", Name("c"), Name("c"))),
                      CmpOp("==", BinOp("*", Name("b"), Name("b")))),
                    Compare(
                      BinOp(
                        "+",
                        BinOp("*", Name("b"), Name("b")),
                        BinOp("*", Name("c"), Name("c"))),
                      CmpOp("==", BinOp("*", Name("a"), Name("a")))))))))
endmodule
