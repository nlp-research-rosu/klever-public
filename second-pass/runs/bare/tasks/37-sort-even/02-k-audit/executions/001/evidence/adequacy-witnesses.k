requires "verification.k"

module ADEQUACY-WITNESSES
  imports VERIFICATION
  imports K-EQUAL

  // Ground substitution for the universal top-level postcondition.
  claim <k>
          pyList(sortEvenReference(L:List))
       => pyList(ListItem(3) ListItem(6) ListItem(5) ListItem(4))
        ...
        </k>
        <program> solutionProgram() </program>
    requires L ==K ListItem(5) ListItem(6) ListItem(3) ListItem(4)
    [label(reference-ground-witness)]

  // Ground helper substitutions exercise empty/base and recursive branches.
  claim <k>
          pyList(evenPositions(L:List))
       => pyList(ListItem(5) ListItem(3))
        ...
        </k>
        <program> solutionProgram() </program>
    requires L ==K ListItem(5) ListItem(6) ListItem(3) ListItem(4)
    [label(even-ground-witness)]

  claim <k>
          pyList(insertReference(pyInt(X:Int), L:List))
       => pyList(ListItem(3) ListItem(5) ListItem(7))
        ...
        </k>
        <program> solutionProgram() </program>
    requires X ==Int 3
     andBool L ==K ListItem(5) ListItem(7)
    [label(insert-front-witness)]

  claim <k>
          pyList(insertReference(pyInt(X:Int), L:List))
       => pyList(ListItem(5) ListItem(6) ListItem(7))
        ...
        </k>
        <program> solutionProgram() </program>
    requires X ==Int 6
     andBool L ==K ListItem(5) ListItem(7)
    [label(insert-middle-witness)]

  claim <k>
          pyList(rebuildReference(L:List, EVENS:List))
       => pyList(ListItem(3) ListItem(6) ListItem(5) ListItem(4))
        ...
        </k>
        <program> solutionProgram() </program>
    requires L ==K ListItem(5) ListItem(6) ListItem(3) ListItem(4)
     andBool EVENS ==K ListItem(3) ListItem(5)
    [label(rebuild-ground-witness)]
endmodule
