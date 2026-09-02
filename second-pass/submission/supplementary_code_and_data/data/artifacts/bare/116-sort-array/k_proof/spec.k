requires "verification.k"

module SPEC
  imports VERIFICATION

  // Interpreter-to-model lemmas for the key functions.  They are parametric
  // in arbitrary mathematical integers, not bounded test values.
  claim [count-correct]:
    <k> evalCall("count_ones", intV(N) ; .Vals, solutionDefs)
      => intV(popcount(N)) </k>

  claim [comparator-correct]:
    <k> evalCall("comes_before", intV(A) ; intV(B) ; .Vals, solutionDefs)
      => boolV(beforeEq(A, B)) </k>
    requires A >=Int 0 andBool B >=Int 0

  claim [insert-empty]:
    <k> evalCall(
          "insert_sorted",
          intV(X) ; listV(.Ints) ; .Vals,
          solutionDefs)
      => listV(insertModel(X, .Ints)) </k>

  claim [insert-at-front]:
    <k> evalCall(
          "insert_sorted",
          intV(X) ; listV(Y :: YS) ; .Vals,
          solutionDefs)
      => listV(insertModel(X, Y :: YS)) </k>
    requires beforeEq(X, Y)

  // Exhaustive symbolic proof for every list of length at most two.  The pair
  // claims cover both possible comparator outcomes for arbitrary A and B.
  claim [sort-empty-symbolic]:
    <k> #run(solutionProgram, listV(.Ints))
      => listV(sortModel(.Ints)) </k>

  claim [sort-singleton-symbolic]:
    <k> #run(solutionProgram, listV(A :: .Ints))
      => listV(sortModel(A :: .Ints)) </k>

  claim [sort-pair-before]:
    <k> #run(solutionProgram, listV(A :: B :: .Ints))
      => listV(sortModel(A :: B :: .Ints)) </k>
    requires beforeEq(A, B)

  claim [sort-pair-after]:
    <k> #run(solutionProgram, listV(A :: B :: .Ints))
      => listV(sortModel(A :: B :: .Ints)) </k>
    requires notBool beforeEq(A, B)

  // For length three, the six claims are the six insertion-sort paths.  Their
  // preconditions partition every possible ordering of A, B, and C.
  claim [sort-triple-abc]:
    <k> #run(solutionProgram, listV(A :: B :: C :: .Ints))
      => listV(sortModel(A :: B :: C :: .Ints)) </k>
    requires beforeEq(B, C) andBool beforeEq(A, B)

  claim [sort-triple-bac]:
    <k> #run(solutionProgram, listV(A :: B :: C :: .Ints))
      => listV(sortModel(A :: B :: C :: .Ints)) </k>
    requires beforeEq(B, C)
      andBool notBool beforeEq(A, B)
      andBool beforeEq(A, C)

  claim [sort-triple-bca]:
    <k> #run(solutionProgram, listV(A :: B :: C :: .Ints))
      => listV(sortModel(A :: B :: C :: .Ints)) </k>
    requires beforeEq(B, C)
      andBool notBool beforeEq(A, B)
      andBool notBool beforeEq(A, C)

  claim [sort-triple-acb]:
    <k> #run(solutionProgram, listV(A :: B :: C :: .Ints))
      => listV(sortModel(A :: B :: C :: .Ints)) </k>
    requires notBool beforeEq(B, C) andBool beforeEq(A, C)

  claim [sort-triple-cab]:
    <k> #run(solutionProgram, listV(A :: B :: C :: .Ints))
      => listV(sortModel(A :: B :: C :: .Ints)) </k>
    requires notBool beforeEq(B, C)
      andBool notBool beforeEq(A, C)
      andBool beforeEq(A, B)

  claim [sort-triple-cba]:
    <k> #run(solutionProgram, listV(A :: B :: C :: .Ints))
      => listV(sortModel(A :: B :: C :: .Ints)) </k>
    requires notBool beforeEq(B, C)
      andBool notBool beforeEq(A, C)
      andBool notBool beforeEq(A, B)

  // Concrete end-to-end consequences through the translated AST.  The first
  // two intentionally distinguish bit-count ordering from ordinary sorting.
  claim [example-one]:
    <k> #run(solutionProgram, listV(1 :: 5 :: 2 :: 3 :: 4 :: .Ints))
      => listV(1 :: 2 :: 4 :: 3 :: 5 :: .Ints) </k>

  claim [example-three]:
    <k> #run(solutionProgram, listV(1 :: 0 :: 2 :: 3 :: 4 :: .Ints))
      => listV(0 :: 1 :: 2 :: 4 :: 3 :: .Ints) </k>

  claim [empty]:
    <k> #run(solutionProgram, listV(.Ints))
      => listV(.Ints) </k>

  claim [duplicates]:
    <k> #run(solutionProgram, listV(3 :: 1 :: 3 :: 0 :: 1 :: .Ints))
      => listV(0 :: 1 :: 1 :: 3 :: 3 :: .Ints) </k>

  claim [wide-popcounts]:
    <k> #run(solutionProgram, listV(7 :: 8 :: 3 :: 2 :: 1 :: 0 :: .Ints))
      => listV(0 :: 1 :: 2 :: 8 :: 3 :: 7 :: .Ints) </k>

  // Total extension used by the implementation for the prompt's negative
  // example: Python-style binary digit count is taken on the magnitude.
  claim [negative-extension]:
    <k> #run(solutionProgram, listV(-2 :: -3 :: -4 :: -5 :: -6 :: .Ints))
      => listV(-4 :: -2 :: -6 :: -5 :: -3 :: .Ints) </k>

  // Independent checks that each demonstrated result has the two defining
  // sorting properties: adjacent key order and unchanged multiplicities.
  claim [example-ordered]:
    <k> ordered(sortModel(1 :: 5 :: 2 :: 3 :: 4 :: .Ints))
      => true </k>

  claim [example-permutation]:
    <k> sameMultiplicity(
          1 :: 5 :: 2 :: 3 :: 4 :: .Ints,
          1 :: 5 :: 2 :: 3 :: 4 :: .Ints,
          sortModel(1 :: 5 :: 2 :: 3 :: 4 :: .Ints))
      => true </k>
endmodule
