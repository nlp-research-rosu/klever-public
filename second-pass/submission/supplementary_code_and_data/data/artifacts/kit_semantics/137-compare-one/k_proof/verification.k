requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact AST emitted in solution.mpy, named only to keep the claims readable.
  syntax Module ::= solutionModule() [function, total]
  rule solutionModule()
    => Module(
         FuncDef("compare_one", Params("a", "b"),
           If(Call(Name("isinstance"), Name("a"), Name("str")),
             Assign(Name("a_value"),
               Call(Name("float"),
                 Call(Attribute(Name("a"), "replace"), Str(","), Str(".")))) .Stmts,
             Assign(Name("a_value"), Name("a")) .Stmts)
           If(Call(Name("isinstance"), Name("b"), Name("str")),
             Assign(Name("b_value"),
               Call(Name("float"),
                 Call(Attribute(Name("b"), "replace"), Str(","), Str(".")))) .Stmts,
             Assign(Name("b_value"), Name("b")) .Stmts)
           If(Compare(Name("a_value"), CmpOp(">", Name("b_value"))),
             Return(Name("a")) .Stmts, .Stmts)
           If(Compare(Name("b_value"), CmpOp(">", Name("a_value"))),
             Return(Name("b")) .Stmts, .Stmts)
           Return(NoneVal) .Stmts))

  // Mathematical reading of each permitted argument under the fixed MPY model.
  // String normalization is exactly the program's replace(",", ".") then float().
  syntax Val ::= numericValue(Val) [function]
  rule numericValue(I:Int)         => I
  rule numericValue(F:Float)       => F
  rule numericValue(str(C:IntSeq)) => decStrToF(replaceC(C, 44, 46))

  // The contract over real numbers: return the original larger argument;
  // if neither is larger, they are equal and None is returned.
  syntax Val ::= expectedCompare(Val, Val) [function]
  rule expectedCompare(A:Val, B:Val) => A
    requires applyCmp(">", numericValue(A), numericValue(B))
  rule expectedCompare(A:Val, B:Val) => B
    requires notBool applyCmp(">", numericValue(A), numericValue(B))
     andBool applyCmp(">", numericValue(B), numericValue(A))
  rule expectedCompare(A:Val, B:Val) => noneV
    requires notBool applyCmp(">", numericValue(A), numericValue(B))
     andBool notBool applyCmp(">", numericValue(B), numericValue(A))
endmodule
