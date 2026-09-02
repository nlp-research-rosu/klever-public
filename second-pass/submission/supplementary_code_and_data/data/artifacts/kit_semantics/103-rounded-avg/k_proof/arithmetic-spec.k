requires "arithmetic-verification.k"

module ARITHMETIC-SPEC
  imports ARITHMETIC-VERIFICATION

  claim [euclidean-reconstruction]:
    <k>
      2 *Int ((V -Int pyMod(V, 2)) /Int 2) +Int pyMod(V, 2)
      => V
    </k>
    requires V >=Int 0

  claim [euclidean-reconstruction-normalized]:
    <k>
      2 *Int ((V -Int ((V %Int 2 +Int 2) %Int 2)) /Int 2)
        +Int ((V %Int 2 +Int 2) %Int 2)
      => V
    </k>
    requires V >=Int 0
endmodule
