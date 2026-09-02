requires "verification.k"

module SPEC
  imports VERIFICATION

  claim <k>
          run(pyList(.List))
        => pyList(.List)
        ...
        </k>
        <program> solutionProgram() </program>
    [label(empty-example)]

  claim <k>
          run(
            pyList(
              ListItem(5) ListItem(6)
              ListItem(3) ListItem(4)))
        => pyList(
             ListItem(3) ListItem(6)
             ListItem(5) ListItem(4))
        ...
        </k>
        <program> solutionProgram() </program>
    [label(prompt-example)]

  claim <k>
          run(pyList(ListItem(1) ListItem(2) ListItem(3)))
        => pyList(ListItem(1) ListItem(2) ListItem(3))
        ...
        </k>
        <program> solutionProgram() </program>
    [label(first-prompt-example)]

  // Together these arbitrary-integer claims cover the two possible orders
  // at length four: B and D stay put, while A and C become ordered.
  claim <k>
          run(pyList(ListItem(A:Int) ListItem(B:Int) ListItem(C:Int) ListItem(D:Int)))
        => pyList(ListItem(A) ListItem(B) ListItem(C) ListItem(D))
        ...
        </k>
        <program> solutionProgram() </program>
    requires A <=Int C
    [label(symbolic-four-ordered)]

  claim <k>
          run(pyList(ListItem(A:Int) ListItem(B:Int) ListItem(C:Int) ListItem(D:Int)))
        => pyList(ListItem(C) ListItem(B) ListItem(A) ListItem(D))
        ...
        </k>
        <program> solutionProgram() </program>
    requires A >Int C
    [label(symbolic-four-reversed)]

  claim <k>
          applyFunction(
            "even_values", ListItem(pyList(L)))
        => pyList(evenPositions(L))
        ...
        </k>
        <program> solutionProgram() </program>
    [label(even-correct)]

  claim <k>
          applyFunction(
            "insert_sorted",
            ListItem(pyInt(X)) ListItem(pyList(L)))
        => pyList(insertReference(pyInt(X), L))
        ...
        </k>
        <program> solutionProgram() </program>
    [label(insert-correct)]

  claim <k>
          applyFunction(
            "sort_values", ListItem(pyList(L)))
        => pyList(sortReference(L))
        ...
        </k>
        <program> solutionProgram() </program>
    [label(sort-correct)]

  claim <k>
          applyFunction(
            "rebuild", ListItem(pyList(L)) ListItem(pyList(EVENS)))
        => pyList(rebuildReference(L, EVENS))
        ...
        </k>
        <program> solutionProgram() </program>
    [label(rebuild-correct)]

  claim <k>
          run(pyList(L))
        => pyList(sortEvenReference(L))
        ...
        </k>
        <program> solutionProgram() </program>
    [label(top-correct)]
endmodule
