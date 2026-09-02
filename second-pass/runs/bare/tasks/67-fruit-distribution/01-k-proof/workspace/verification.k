requires "semantic.k"

module VERIFICATION
  imports MPY-SEMANTIC

  // This is the constructor term emitted in solution.mpy.  Keeping it here
  // makes the proof claim independent of parser/configuration initializers.
  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(
      FuncDef("fruit_distribution", Params("s", "n"),
        Assign(Name("words"), Call(Attribute(Name("s"), "split"), ))
        Return(
          BinOp(
            "-",
            BinOp(
              "-",
              Name("n"),
              Call(Name("int"), Subscript(Name("words"), Int(0)))),
            Call(Name("int"), Subscript(Name("words"), Int(3)))))))

  syntax KItem ::= "runFruit" "(" Program "," Int "," Int "," Int ")"
                 | "runString" "(" Program "," String "," Int ")"

  rule runFruit(P:Program, A:Int, O:Int, N:Int)
    => P ~> invokeFruit(A, O, N)

  rule runString(P:Program, S:String, N:Int)
    => P ~> invokeString(S, N)
endmodule
