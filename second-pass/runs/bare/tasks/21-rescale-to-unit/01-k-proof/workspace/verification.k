requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Algebraic simplifications needed by the symbolic backend for Rat terms.
  // They are consequences of the RAT domain and are applied only to defined
  // divisions.
  rule R +Rat (-1 *Rat R) => 0 [simplification]
  rule R /Rat R => 1 requires R =/=Rat 0 [simplification]
  rule 0 /Rat R => 0 requires R =/=Rat 0 [simplification]

  // This is the exact constructor tree generated in solution.mpy.  Keeping it
  // as a function makes the claims readable; prove.sh regenerates and runs the
  // actual solution.mpy before invoking these proofs.
  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      ImportFrom("typing", "List", .Strings)
      FuncDef("rescale_to_unit", Params("numbers", .Strings),
        CellVars("maximum", "minimum", .Strings), FreeVars(.Strings),
        Assign(Name("minimum"), Call(Name("min"), Name("numbers")))
        Assign(Name("maximum"), Call(Name("max"), Name("numbers")))
        Return(
          ListComp(
            BinOp("/",
              BinOp("-", Name("number"), Name("minimum")),
              BinOp("-", Name("maximum"), Name("minimum"))),
            CompFor(Name("number"), Name("numbers"), Bool(true))))
        .Stmts)
      .Stmts)

  // Proof-only wrapper: execute the ordinary operational semantics, collect
  // the returned value, and restore the auxiliary cells to their initial
  // values.  This lets a claim focus on the observable function result.
  syntax KItem ::= verify(Program, Value) | "collect" | done(Value)

  rule <k> verify(Module(SS), ARG)
         => exec(SS) ~> invoke("rescale_to_unit", ARG) ~> collect
       </k>

  rule <k> collect => done(V) </k>
       <functions> _ => .Map </functions>
       <env> _ => .Map </env>
       <result> V => noResult </result>

  // An independent, mathematical statement of the contract.  It uses only
  // minimum, maximum, and pointwise affine scaling over exact rationals.
  syntax Value ::= rescaleSpec(Value) [function]
  syntax Rats ::= scaleRats(Rats, Rat, Rat) [function]

  rule rescaleSpec(vlist(H, T))
    => vlist(scaleRats(H, T, minRats(H, T), maxRats(H, T)))

  rule scaleRats(.Rats, _, _) => .Rats
  rule scaleRats(X, XS, LO, HI)
    => ((X -Rat LO) /Rat (HI -Rat LO)), scaleRats(XS, LO, HI)
    requires HI =/=Rat LO
endmodule
