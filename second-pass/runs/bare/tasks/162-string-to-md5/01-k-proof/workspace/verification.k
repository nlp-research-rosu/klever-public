requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // This is the exact constructor tree emitted in solution.mpy, factored out
  // so every claim verifies the same translated program.
  syntax Stmts ::= "solutionBody" [function]
  rule solutionBody =>
    Return(
      IfExp(
        Compare(Name("text"), CmpOp("==", Str(""))),
        NoneVal,
        Call(
          Attribute(
            Call(
              Attribute(Name("hashlib"), "md5"),
              Call(Attribute(Name("text"), "encode"), )),
            "hexdigest"),
          )))
    .Stmts

  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      Import("hashlib")
      FuncDef("string_to_md5", Params("text"), solutionBody))

  // Mathematical result used by the symbolic non-empty contract.
  syntax PyValue ::= "expectedMd5" "(" String ")" [function]
  rule expectedMd5(S) => pyString(md5String(S))
endmodule
