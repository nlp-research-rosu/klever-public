// Reviewer body-sensitivity mutation: the list-comprehension numerator uses
// maximum rather than the iterated number. The claim executes this changed AST.
requires "semantic.k"

module VERIFICATION-BODY-MUTANT
  imports SEMANTIC

  rule R +Rat (-1 *Rat R) => 0 [simplification]
  rule R /Rat R => 1 requires R =/=Rat 0 [simplification]
  rule 0 /Rat R => 0 requires R =/=Rat 0 [simplification]

  syntax Program ::= "mutantProgram" [function]
  rule mutantProgram =>
    Module(
      ImportFrom("typing", "List", .Strings)
      FuncDef("rescale_to_unit", Params("numbers", .Strings),
        CellVars("maximum", "minimum", .Strings), FreeVars(.Strings),
        Assign(Name("minimum"), Call(Name("min"), Name("numbers")))
        Assign(Name("maximum"), Call(Name("max"), Name("numbers")))
        Return(
          ListComp(
            BinOp("/",
              BinOp("-", Name("maximum"), Name("minimum")),
              BinOp("-", Name("maximum"), Name("minimum"))),
            CompFor(Name("number"), Name("numbers"), Bool(true))))
        .Stmts)
      .Stmts)

  syntax KItem ::= verifyMutant(Program, Value) | "collectMutant" | doneMutant(Value)

  rule <k> verifyMutant(Module(SS), ARG)
         => exec(SS) ~> invoke("rescale_to_unit", ARG) ~> collectMutant
       </k>

  rule <k> collectMutant => doneMutant(V) </k>
       <functions> _ => .Map </functions>
       <env> _ => .Map </env>
       <result> V => noResult </result>
endmodule
