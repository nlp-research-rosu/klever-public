requires "verification.k"

module SPEC
  imports MPY-SEMANTIC
  imports SORTED-LIST-VERIFICATION

  // Universal functional-correctness theorem for every finite Words value.
  // The specification is filter-even followed by ascending (length, text)
  // sorting, with duplicates retained.
  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"), ValueExpr(VList(INPUT:Words))))
        => Result(VList(sortedListSumSpec(INPUT)))
        </k>
    [label(universal-correctness)]

  // The empty-list base case.
  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"), ValueExpr(VList(.Words))))
        => Result(VList(evenSorted(.Words)))
        </k>
    [label(base)]

  // Symbolic strings exercise both parity filtering and both ordering keys.
  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"),
              ValueExpr(VList(A:String, B:String))))
        => Result(VList(evenSorted(A, B)))
        </k>
    requires lengthString(A) ==Int 2
     andBool lengthString(B) ==Int 2
     andBool A <String B
    [label(symbolic-two)]

  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"),
              ValueExpr(VList(A:String, B:String))))
        => Result(VList(evenSorted(A, B)))
        </k>
    requires lengthString(A) ==Int 2
     andBool lengthString(B) ==Int 2
     andBool notBool (A <String B)
    [label(symbolic-two-reverse)]

  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"),
              ValueExpr(VList(A:String, B:String, C:String))))
        => Result(VList(evenSorted(A, B, C)))
        </k>
    requires lengthString(A) ==Int 4
     andBool lengthString(B) ==Int 2
     andBool lengthString(C) ==Int 3
    [label(symbolic-three)]

  // Both examples stated in prompt.py.
  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"),
              ListExpr(Str("aa"), Str("a"), Str("aaa"))))
        => Result(VList("aa"))
        </k>
    [label(prompt-example-one)]

  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"),
              ListExpr(Str("ab"), Str("a"), Str("aaa"), Str("cd"))))
        => Result(VList("ab", "cd"))
        </k>
    [label(prompt-example-two)]
endmodule
