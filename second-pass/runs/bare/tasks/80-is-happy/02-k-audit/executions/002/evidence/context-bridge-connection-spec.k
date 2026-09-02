requires "semantic.k"

module AUDIT-CONTEXT-BRIDGE-CONNECTIONS
  imports MPY-SEMANTIC

  // These claims use the semantics with the six contextual #choose shortcuts
  // removed. KONT makes the accepted continuation context explicit.
  claim <k> #choose(#short3(eps), YES, NO, REST, P, V, PGM)
             ~> KONT:K
          => #branch(YES, REST, P, V, PGM)
             ~> KONT
        </k>

  claim <k> #choose(#short3(ch(A, eps)), YES, NO, REST, P, V, PGM)
             ~> KONT:K
          => #branch(YES, REST, P, V, PGM)
             ~> KONT
        </k>

  claim <k> #choose(#short3(ch(A, ch(B, eps))), YES, NO, REST, P, V, PGM)
             ~> KONT:K
          => #branch(YES, REST, P, V, PGM)
             ~> KONT
        </k>

  claim <k> #choose(#short3(ch(A, ch(B, ch(C, TAIL)))),
                    YES, NO, REST, P, V, PGM)
             ~> KONT:K
          => #branch(NO, REST, P, V, PGM)
             ~> KONT
        </k>

  claim <k> #choose(#same(I, I), YES, NO, REST, P, V, PGM)
             ~> KONT:K
          => #branch(YES, REST, P, V, PGM)
             ~> KONT
        </k>

  claim <k> #choose(#same(I, J), YES, NO, REST, P, V, PGM)
             ~> KONT:K
          => #branch(NO, REST, P, V, PGM)
             ~> KONT
        </k>
    requires I =/=Int J
endmodule
