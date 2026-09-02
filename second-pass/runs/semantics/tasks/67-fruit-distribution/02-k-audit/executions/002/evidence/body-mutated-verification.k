requires "reference-semantics/semantics.k"

module BODY-MUTATED-VERIFICATION
  imports MPY

  // Symbolic decimal encodings.  These terms stand for the ASCII decimal
  // representation of a non-negative integer and for the contract's exact
  // "<a> apples and <b> oranges" sentence shape, respectively.
  syntax IntSeq ::= decimalCodes(Int)
                  | fruitSentenceCodes(Int, Int)

  // MPY-METHODS deliberately makes split concrete and calls for a
  // problem-local interception on symbolic strings.  This is that
  // interception for precisely the input grammar in prompt.py.
  rule <k>
         #applyK(
           toCall(boundMethodV(str(fruitSentenceCodes(A, B)), "split")),
           .Vals)
         => #alloc(
              list(
                vCons(str(decimalCodes(A)),
                vCons(str(strToCodes("apples")),
                vCons(str(strToCodes("and")),
                vCons(str(decimalCodes(B)),
                vCons(str(strToCodes("oranges")), .ValSeq)))))))
         ...
       </k>
    requires A >=Int 0 andBool B >=Int 0
    [priority(30)]

  // Decimal decoding is the inverse observation needed by this task.  The
  // concrete examples do not use this abstraction: krun and their proof
  // claims exercise MPY-BUILTINS's actual Horner-fold implementation.
  rule applyBuiltin("int", str(decimalCodes(I)), .Vals) => I
    requires I >=Int 0
    [priority(30)]

  // This is exactly the constructor tree generated in solution.mpy.  Keeping
  // it as one named function makes spec.k readable while the proof still
  // executes every statement and expression in the translated implementation.
  syntax Module ::= "solutionModule" [function, total]
  rule solutionModule =>
    Module(
      FuncDef("fruit_distribution", Params("s", "n"),
        Assign(
          Name("fruits"),
          Call(Attribute(Name("s"), "split"), .Exprs))
        Return(
          BinOp(
            "-",
            BinOp(
              "-",
              Name("n"),
              Call(
                Name("int"),
                Subscript(Name("fruits"), Int(0)), .Exprs)),
            Call(
              Name("int"),
              Subscript(Name("fruits"), Int(0)), .Exprs)))))
endmodule
