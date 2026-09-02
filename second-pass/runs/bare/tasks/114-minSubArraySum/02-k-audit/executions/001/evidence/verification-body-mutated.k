requires "semantic.k"

module VERIFICATION-BODY-MUTATED
  imports MPY

  // minPrefix is the least sum of a non-empty prefix.  Every non-empty prefix
  // of H :: T is either [H], or H followed by a non-empty prefix of T.
  // minSubarray is the least sum of any non-empty contiguous subarray.  Such a
  // subarray either starts at H (and is covered by minPrefix) or lies in T.
  // These constructor equations therefore state the HumanEval contract.
  syntax Int ::= minPrefix(IntList) [function]
               | minSubarray(IntList) [function]
  rule minPrefix(cons(H, nil)) => H
  rule minPrefix(cons(H, cons(J, T)))
    => intMin(H, H +Int minPrefix(cons(J, T)))
  rule minSubarray(cons(H, nil)) => H
  rule minSubarray(cons(H, cons(J, T)))
    => intMin(minSubarray(cons(J, T)),
              minPrefix(cons(H, cons(J, T))))

  // A literal copy of solution.mpy as a function map and as a module term.
  // The end-to-end claims start from solutionProgram; call-level claims use
  // solutionFunctions as circular lemmas for the two recursive definitions.
  syntax Map ::= "solutionFunctions" [function]
  rule solutionFunctions =>
      ("min_prefix_sum" |-> closure(Params("nums"),
        If(Compare(Call(Name("len"), Name("nums")), CmpOp("==", Int(1))),
          Return(Subscript(Name("nums"), Int(0))),
          .Stmts)
        Assign(Name("tail_min"),
          Call(Name("min_prefix_sum"),
            Subscript(Name("nums"), Slice(Int(1), NoBound, NoBound))))
        Return(Call(Name("min"),
          Subscript(Name("nums"), Int(0)),
          BinOp("+", Subscript(Name("nums"), Int(0)), Name("tail_min"))))))
      ("minSubArraySum" |-> closure(Params("nums"),
        If(Compare(Call(Name("len"), Name("nums")), CmpOp("==", Int(1))),
          Return(Int(0)),
          .Stmts)
        Assign(Name("tail_min"),
          Call(Name("minSubArraySum"),
            Subscript(Name("nums"), Slice(Int(1), NoBound, NoBound))))
        Assign(Name("prefix_min"),
          Call(Name("min_prefix_sum"), Name("nums")))
        Return(Call(Name("min"), Name("tail_min"), Name("prefix_min")))))

  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram => Module(
    FuncDef("min_prefix_sum", Params("nums"),
      If(Compare(Call(Name("len"), Name("nums")), CmpOp("==", Int(1))),
        Return(Subscript(Name("nums"), Int(0))),
        .Stmts)
      Assign(Name("tail_min"),
        Call(Name("min_prefix_sum"),
          Subscript(Name("nums"), Slice(Int(1), NoBound, NoBound))))
      Return(Call(Name("min"),
        Subscript(Name("nums"), Int(0)),
        BinOp("+", Subscript(Name("nums"), Int(0)), Name("tail_min")))))
    FuncDef("minSubArraySum", Params("nums"),
      If(Compare(Call(Name("len"), Name("nums")), CmpOp("==", Int(1))),
        Return(Int(0)),
        .Stmts)
      Assign(Name("tail_min"),
        Call(Name("minSubArraySum"),
          Subscript(Name("nums"), Slice(Int(1), NoBound, NoBound))))
      Assign(Name("prefix_min"),
        Call(Name("min_prefix_sum"), Name("nums")))
      Return(Call(Name("min"), Name("tail_min"), Name("prefix_min"))))
  )
endmodule
