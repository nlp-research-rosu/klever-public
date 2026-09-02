requires "reference-semantics/semantics.k"

module VERIFICATION-WRONGINT
  imports MPY

  syntax IntSeq ::= decimalCodes(Int)
                  | fruitSentenceCodes(Int, Int)

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

  // Deliberately false opposite interpretation used only for sensitivity:
  // the decimal token I is decoded as I+1.
  rule applyBuiltin("int", str(decimalCodes(I)), .Vals) => I +Int 1
    requires I >=Int 0
    [priority(30)]

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
              Subscript(Name("fruits"), Int(3)), .Exprs)))))
endmodule
