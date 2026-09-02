requires "semantic.k"

module VERIFICATION
  imports SEMANTIC
  imports K-EQUAL

  syntax Pgm ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("filter_by_substring",
        Params("strings", "substring"),
        CellVars("substring"),
        FreeVars(),
        Return(
          ListComp(Name("string"),
            CompFor(
              Name("string"),
              Name("substring"),
              Compare(Name("substring"), CmpOp("in", Name("string"))))))))

  syntax PyList ::= filterRef(PyList, String) [function, total]
  rule filterRef(Nil, _SUBSTRING) => Nil
  rule filterRef(Cons(HEAD, TAIL), SUBSTRING)
    => Cons(HEAD, filterRef(TAIL, SUBSTRING))
    requires containsString(HEAD, SUBSTRING)
  rule filterRef(Cons(HEAD, TAIL), SUBSTRING)
    => filterRef(TAIL, SUBSTRING)
    requires notBool containsString(HEAD, SUBSTRING)
endmodule
