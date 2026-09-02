requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Deallocating a fresh call frame restores the surrounding scope map. This
  // is the symbolic form of the concrete Map update simplification used by
  // MPY-FUNCTIONS.#pop.
  rule ((L:Int |-> _V:Scope) M:Map) [ L <- undef ] => M
    requires notBool (L in_keys(M))
    [simplification]

  // The exact constructor term generated from solution.py, named so that the
  // proof claim can start from the same module that krun parses.
  syntax Module ::= "solutionModule" [macro]
  rule solutionModule
    => Module(
         FuncDef("largest_prime_factor", Params("n"),
           Assign(Name("factor"), Int(2))
           While(Compare(Name("n"), CmpOp(">", Name("factor"))),
             If(Compare(
               BinOp("%", Name("n"), Name("factor")),
               CmpOp("==", Int(0))),
               Assign(Name("n"),
                 BinOp("//", Name("n"), Name("factor"))),
               AugAssign(Name("factor"), "+", Int(1))))
           Return(Name("factor"))))

  // Names for the loop fragments used by the circular loop claim.
  syntax Expr ::= "lpfCondition" [macro]
  rule lpfCondition
    => Compare(Name("n"), CmpOp(">", Name("factor")))

  syntax Stmts ::= "lpfStep" [macro]
  rule lpfStep
    => If(Compare(
         BinOp("%", Name("n"), Name("factor")),
         CmpOp("==", Int(0))),
         Assign(Name("n"), BinOp("//", Name("n"), Name("factor"))),
         AugAssign(Name("factor"), "+", Int(1)))

  // Independent mathematical recurrence for trial division. The loop proof
  // establishes that the Python execution refines this specification.
  syntax Int ::= lpfSpec(Int, Int) [function, total]
  rule lpfSpec(N:Int, F:Int) => F
    requires N <=Int F
  rule lpfSpec(N:Int, F:Int)
    => lpfSpec((N -Int pyMod(N, F)) /Int F, F)
    requires N >Int F andBool pyMod(N, F) ==Int 0
  rule lpfSpec(N:Int, F:Int) => lpfSpec(N, F +Int 1)
    requires N >Int F andBool pyMod(N, F) =/=Int 0

  // Symbolic accelerator rules derived directly from the MPY rules. The
  // Haskell backend cannot cool a symbolic Int through generated strictness
  // freezers in this semantics, so these rules collapse only the exact
  // integer redexes used by this program. They preserve the reference
  // semantics' lookup, pyMod, floor-division, assignment, and return effects.
  rule <k>
         Compare(Name("n"), CmpOp(">", Name("factor")))
         => N >Int F
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("n" |-> N:Int) ("factor" |-> F:Int) _REST:Map,
           _P:Parent)
         ...
       </scopes>
       [priority(40)]

  rule <k>
         Compare(
           BinOp("%", Name("n"), Name("factor")),
           CmpOp("==", Int(0)))
         => pyMod(N, F) ==Int 0
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("n" |-> N:Int) ("factor" |-> F:Int) _REST:Map,
           _P:Parent)
         ...
       </scopes>
       [priority(40)]

  rule <k>
         Assign(Name("n"), BinOp("//", Name("n"), Name("factor")))
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("n" |-> N:Int) ("factor" |-> F:Int) REST:Map
           => ("n" |-> ((N -Int pyMod(N, F)) /Int F))
              ("factor" |-> F) REST,
           _P:Parent)
         ...
       </scopes>
       [priority(40)]

  rule <k>
         AugAssign(Name("factor"), "+", Int(1))
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("n" |-> N:Int) ("factor" |-> F:Int) REST:Map
           => ("n" |-> N) ("factor" |-> (F +Int 1)) REST,
           _P:Parent)
         ...
       </scopes>
       [priority(40)]

  rule <k> Return(Name("factor")) ~> _ => #pop </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("factor" |-> F:Int) _REST:Map,
           _P:Parent)
         ...
       </scopes>
       <ret> noRet => retV(F) </ret>
       [priority(40)]
endmodule
