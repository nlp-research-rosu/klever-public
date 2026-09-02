requires "reference-semantics/semantics.k"

module VERIFICATION-MUTATED-BODY
  imports MPY

  // Proof summary for the exact normalization expression used below.
  // The reference decimal parser has a concrete Int2Float implementation,
  // whose hook is deliberately unavailable in the Haskell prover.  This
  // symbol denotes decStrToF(replaceC(CS, 44, 46)); the k-cell interception
  // keeps that operation opaque only in this symbolic definition.
  syntax Float ::= commaDecimal(IntSeq)
    [function, total, symbol(commaDecimal), no-evaluators]
  syntax KItem ::= "#commaDecimal"
  rule <k> Call(Name("float"),
                (Call(Attribute(E:Expr, "replace"), Str(","), Str("."), .Exprs),
                 .Exprs))
        => E ~> #commaDecimal ... </k>
    [priority(40)]
  rule <k> str(CS:IntSeq) ~> #commaDecimal => commaDecimal(CS) ... </k>

  // The reference Float equality rule delegates to a FLOAT.eq hook that the
  // Haskell backend also lacks.  Keep symbolic float equality as one Boolean
  // atom; LLVM still evaluates the supplied reference rule concretely.
  syntax Bool ::= sameFloat(Float, Float)
    [function, total, symbol(sameFloat), no-evaluators]
  rule <k> Compare(A:Float, CmpOp("==", B:Float))
        => sameFloat(A, B) ... </k>
    [priority(40)]

  // The exact translated function body, packaged as a symbolic entry point.
  // It is called through the normal closure/frame machinery.  The surrounding
  // concrete initial configuration in spec.k supplies the module and builtins
  // scopes that loading solution.mpy would establish around this function.
  syntax KItem ::= runCompare(Val, Val)
  rule runCompare(A:Val, B:Val)
    => #applyK(toCall(closureVal(("a", "b", .ParamNames),
         Assign(Name("a_value"), Name("a"))
         Assign(Name("b_value"), Name("b"))
         If(Call(Name("isinstance"), Name("a"), Name("str")),
           Assign(Name("a_value"),
             Call(Name("float"),
               Call(Attribute(Name("a"), "replace"), Str(","), Str(".")))),
           .Stmts)
         If(Call(Name("isinstance"), Name("b"), Name("str")),
           Assign(Name("b_value"),
             Call(Name("float"),
               Call(Attribute(Name("b"), "replace"), Str(","), Str(".")))),
           .Stmts)
         If(Compare(Name("a_value"), CmpOp("==", Name("b_value"))),
           Return(NoneVal),
           .Stmts)
         If(Compare(Name("a_value"), CmpOp(">", Name("b_value"))),
           Return(Name("a")),
           .Stmts)
         Return(Name("a")),
         0)),
       (A, B, .Vals))

  // Contract-level numeric interpretation of the three admitted input forms.
  syntax Val ::= numericValue(Val) [function]
  rule numericValue(I:Int) => I
  rule numericValue(F:Float) => F
  rule numericValue(str(CS:IntSeq)) => commaDecimal(CS)

  syntax Bool ::= numericEqual(Val, Val) [function]
  rule numericEqual(A:Int, B:Int) => A ==Int B
  rule numericEqual(A:Int, B:Float) => eqF(intToF(A), B)
  rule numericEqual(A:Float, B:Int) => eqF(A, intToF(B))
  rule numericEqual(A:Float, B:Float) => sameFloat(A, B)

  // Return None on numeric equality; otherwise preserve and return the
  // original argument whose interpreted numeric value is larger.
  syntax Val ::= expectedCompare(Val, Val) [function]
  rule expectedCompare(A:Val, B:Val)
    => #if numericEqual(numericValue(A), numericValue(B))
       #then noneV
       #else #if applyCmp(">", numericValue(A), numericValue(B))
             #then A
             #else B
             #fi
       #fi
endmodule
