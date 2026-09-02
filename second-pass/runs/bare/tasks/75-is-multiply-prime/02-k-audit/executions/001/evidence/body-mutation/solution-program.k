requires "semantic.k"

module SOLUTION-PROGRAM
  imports MPY-SYNTAX

  // This term is the py2mpy.py translation in solution.mpy.  prove.sh checks
  // the translation's digest before proving, so the proof cannot drift from
  // the executable Python artifact unnoticed.
  syntax Pgm ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef("is_multiply_prime", Params("a"),
        Return(
          BoolOp(
            "or",
            Compare(Name("a"), CmpOp("==", Int(8))),
            Compare(Name("a"), CmpOp("==", Int(12))),
            Compare(Name("a"), CmpOp("==", Int(18))),
            Compare(Name("a"), CmpOp("==", Int(20))),
            Compare(Name("a"), CmpOp("==", Int(27))),
            Compare(Name("a"), CmpOp("==", Int(28))),
            Compare(Name("a"), CmpOp("==", Int(31))),
            Compare(Name("a"), CmpOp("==", Int(42))),
            Compare(Name("a"), CmpOp("==", Int(44))),
            Compare(Name("a"), CmpOp("==", Int(45))),
            Compare(Name("a"), CmpOp("==", Int(50))),
            Compare(Name("a"), CmpOp("==", Int(52))),
            Compare(Name("a"), CmpOp("==", Int(63))),
            Compare(Name("a"), CmpOp("==", Int(66))),
            Compare(Name("a"), CmpOp("==", Int(68))),
            Compare(Name("a"), CmpOp("==", Int(70))),
            Compare(Name("a"), CmpOp("==", Int(75))),
            Compare(Name("a"), CmpOp("==", Int(76))),
            Compare(Name("a"), CmpOp("==", Int(78))),
            Compare(Name("a"), CmpOp("==", Int(92))),
            Compare(Name("a"), CmpOp("==", Int(98))),
            Compare(Name("a"), CmpOp("==", Int(99)))))))
endmodule
