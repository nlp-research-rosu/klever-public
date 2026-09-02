requires "semantic.k"

module MPY-VERIFICATION
  imports MPY

  // Audit mutation: the executed function body now always returns [].
  syntax Module ::= solutionModule() [function]
  rule solutionModule()
    => Module(
         ImportFrom("typing", "List", "Any")
         FuncDef("filter_integers", Params("values"),
           Return(ListExpr(.Exprs))))

  syntax Expr ::= filterExpression() [function]
  rule filterExpression()
    => ListComp(Name("value"),
         CompFor(Name("value"), Name("values"),
           filterCondition()))

  syntax Expr ::= filterCondition() [function]
  rule filterCondition()
    => Call(Name("isinstance"), Name("value"), Name("int"))

  syntax PyVals ::= onlyIntegerInstances(PyVals) [function, total]
  rule onlyIntegerInstances(.PyVals) => .PyVals
  rule onlyIntegerInstances(VInt(I), VS)
    => VInt(I), onlyIntegerInstances(VS)
  rule onlyIntegerInstances(VBool(B), VS)
    => VBool(B), onlyIntegerInstances(VS)
  rule onlyIntegerInstances(VString(_), VS)
    => onlyIntegerInstances(VS)
  rule onlyIntegerInstances(VFloat(_), VS)
    => onlyIntegerInstances(VS)
  rule onlyIntegerInstances(VList(_), VS)
    => onlyIntegerInstances(VS)
  rule onlyIntegerInstances(VDict, VS)
    => onlyIntegerInstances(VS)
  rule onlyIntegerInstances(VNone, VS)
    => onlyIntegerInstances(VS)
  rule onlyIntegerInstances(VOpaque(_), VS)
    => onlyIntegerInstances(VS)

  syntax Bool ::= containsOnlyIntegerInstances(PyVals) [function, total]
  rule containsOnlyIntegerInstances(.PyVals) => true
  rule containsOnlyIntegerInstances(VInt(_), VS)
    => containsOnlyIntegerInstances(VS)
  rule containsOnlyIntegerInstances(VBool(_), VS)
    => containsOnlyIntegerInstances(VS)
  rule containsOnlyIntegerInstances(_, _) => false [owise]
endmodule
