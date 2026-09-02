requires "verification.k"

module MUTATION
  imports VERIFICATION

  // Material body mutation: discard the computed accumulator and always
  // return None.  The body-sensitivity probe must reject result 2 for [1, 2].
  syntax Stmts ::= "mutantBody" [function]
  rule mutantBody =>
    Expr(Str("\n    Return the second-smallest distinct integer in lst, or None when it\n    does not exist.\n    "))
    Assign(Name("found_smallest"), Bool(false))
    Assign(Name("found_second"), Bool(false))
    Assign(Name("smallest"), Int(0))
    Assign(Name("second"), Int(0))
    Assign(Name("x"), Int(0))
    For(Name("x"), Name("lst"), nextSmallestLoopBody)
    Return(NoneVal)
endmodule
