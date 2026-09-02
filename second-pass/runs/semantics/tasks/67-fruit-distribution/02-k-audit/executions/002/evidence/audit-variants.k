requires "reference-semantics/semantics.k"

module AUDIT-COMMON
  imports MPY

  syntax IntSeq ::= decimalCodes(Int)
                  | fruitSentenceCodes(Int, Int)

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

// No proof-local operational bridges: the fixed semantics alone must connect
// the synthetic code constructors to split/int if such a connection exists.
module BRIDGE-FREE
  imports AUDIT-COMMON
endmodule

// Opposite result-bearing interpretation for decimalCodes: each abstract
// numeral decodes one greater than its parameter.
module OPPOSITE-INT
  imports AUDIT-COMMON

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

  rule applyBuiltin("int", str(decimalCodes(I)), .Vals) => I +Int 1
    requires I >=Int 0
    [priority(30)]
endmodule

// Opposite result-bearing interpretation for fruitSentenceCodes: split
// fabricates A+1 as the first numeric token.
module OPPOSITE-SPLIT
  imports AUDIT-COMMON

  rule <k>
         #applyK(
           toCall(boundMethodV(str(fruitSentenceCodes(A, B)), "split")),
           .Vals)
         => #alloc(
              list(
                vCons(str(decimalCodes(A +Int 1)),
                vCons(str(strToCodes("apples")),
                vCons(str(strToCodes("and")),
                vCons(str(decimalCodes(B)),
                vCons(str(strToCodes("oranges")), .ValSeq)))))))
         ...
       </k>
    requires A >=Int 0 andBool B >=Int 0
    [priority(30)]

  rule applyBuiltin("int", str(decimalCodes(I)), .Vals) => I
    requires I >=Int 0
    [priority(30)]
endmodule
