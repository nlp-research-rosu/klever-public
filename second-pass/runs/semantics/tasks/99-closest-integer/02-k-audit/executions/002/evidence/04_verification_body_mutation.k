requires "reference-semantics/semantics.k"

module CLOSEST-INTEGER-VERIFICATION
  imports MPY

  // This is the FuncDef body emitted in solution.mpy.  Keeping the program
  // syntax here makes the reachability claim execute the submitted algorithm,
  // rather than replacing the call with a specification-only summary.
  syntax Stmts ::= "closestBody" "(" ")" [function, total]
  rule closestBody()
    => Assign(Name("number"), Call(Name("float"), Name("value")))
       If(Compare(Name("number"), CmpOp(">", Float(0.0))),
          Return(Call(Name("int"),
                      BinOp("+", Name("number"), Float(1.5)))),
          .Stmts)
       Return(Call(Name("int"),
                   BinOp("-", Name("number"), Float(0.5))))

  // Execute the body as an ordinary one-argument Python closure.
  syntax KItem ::= "runClosest" "(" Str ")"
  rule runClosest(S:Str)
    => Call(closureVal(("value", .ParamNames), closestBody(), 0),
            (S, .Exprs))

  // Contract oracle in terms of the reference semantics' trusted float
  // primitives.  Python int(float) truncates toward zero, so shifting by
  // one half in the direction away from zero implements nearest rounding
  // with half-way cases resolved away from zero.
  syntax Int ::= nearestAway(Float) [function, total]
  rule nearestAway(F:Float)
    => #if gtF(F, 0.0)
       #then truncF(addF(F, 0.5))
       #else truncF(subF(F, 0.5))
       #fi
endmodule
