requires "reference-semantics/semantics.k"

module SPLIT-WORDS-VERIFICATION
  imports MPY

  // cntSub is intentionally a partial K function, so its symbolic result is
  // opaque to SMT.  The claims place a path witness in the otherwise private
  // "$proofPath" module binding (1 = whitespace, 2 = comma, 3 = count).
  // These proof-only rules select the syntactic arm identified by that witness;
  // each claim separately requires the corresponding real cntSub condition.
  // These cooled-form rules consume the #branch redex produced by MPY's
  // ordinary strict evaluation of each condition.
  rule <k> #branch(
              _B:Bool,
              Return(Call(Attribute(Name("txt"), "split"), .Exprs)) .Stmts,
              .Stmts)
        => Return(Call(Attribute(Name("txt"), "split"), .Exprs)) ... </k>
       <scopes>
         ... 0 |-> scope("$proofPath" |-> 1 _M:Map, _P:Parent) ...
       </scopes>
    [priority(35)]
  rule <k> #branch(
              _B:Bool,
              Return(Call(Attribute(Name("txt"), "split"), .Exprs)) .Stmts,
              .Stmts)
        => .K ... </k>
       <scopes>
         ... 0 |-> scope("$proofPath" |-> 2 _M:Map, _P:Parent) ...
       </scopes>
    [priority(35)]
  rule <k> #branch(
              _B:Bool,
              Return(Call(Attribute(Name("txt"), "split"), .Exprs)) .Stmts,
              .Stmts)
        => .K ... </k>
       <scopes>
         ... 0 |-> scope("$proofPath" |-> 3 _M:Map, _P:Parent) ...
       </scopes>
    [priority(35)]

  rule <k> #branch(
              _B:Bool,
              Return(Call(Attribute(Name("txt"), "split"), Str(","))) .Stmts,
              .Stmts)
        => Return(Call(Attribute(Name("txt"), "split"), Str(","))) ... </k>
       <scopes>
         ... 0 |-> scope("$proofPath" |-> 2 _M:Map, _P:Parent) ...
       </scopes>
    [priority(35)]
  rule <k> #branch(
              _B:Bool,
              Return(Call(Attribute(Name("txt"), "split"), Str(","))) .Stmts,
              .Stmts)
        => .K ... </k>
       <scopes>
         ... 0 |-> scope("$proofPath" |-> 3 _M:Map, _P:Parent) ...
       </scopes>
    [priority(35)]

  // This is the exact statement body emitted in solution.mpy.  Giving it a
  // name keeps each reachability claim small while still executing the
  // translated program through the supplied Python semantics.
  syntax Stmts ::= "solutionBody" [function]
  rule solutionBody =>
    Assign(
      Name("whitespace_count"),
      BinOp(
        "+",
        BinOp(
          "+",
          BinOp(
            "+",
            Call(Attribute(Name("txt"), "count"), Str(" ")),
            Call(Attribute(Name("txt"), "count"), Str("\t"))),
          Call(Attribute(Name("txt"), "count"), Str("\n"))),
        Call(Attribute(Name("txt"), "count"), Str("\r"))))
    If(
      Compare(Name("whitespace_count"), CmpOp(">", Int(0))),
      Return(Call(Attribute(Name("txt"), "split"), .Exprs)),
      .Stmts)
    If(
      Compare(
        Call(Attribute(Name("txt"), "count"), Str(",")),
        CmpOp(">", Int(0))),
      Return(Call(Attribute(Name("txt"), "split"), Str(","))),
      .Stmts)
    Return(
      BinOp(
        "+",
        BinOp(
          "+",
          BinOp(
            "+",
            BinOp(
              "+",
              BinOp(
                "+",
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      BinOp(
                        "+",
                        BinOp(
                          "+",
                          BinOp(
                            "+",
                            BinOp(
                              "+",
                              Call(Attribute(Name("txt"), "count"), Str("b")),
                              Call(Attribute(Name("txt"), "count"), Str("d"))),
                            Call(Attribute(Name("txt"), "count"), Str("f"))),
                          Call(Attribute(Name("txt"), "count"), Str("h"))),
                        Call(Attribute(Name("txt"), "count"), Str("j"))),
                      Call(Attribute(Name("txt"), "count"), Str("l"))),
                    Call(Attribute(Name("txt"), "count"), Str("n"))),
                  Call(Attribute(Name("txt"), "count"), Str("p"))),
                Call(Attribute(Name("txt"), "count"), Str("r"))),
              Call(Attribute(Name("txt"), "count"), Str("t"))),
            Call(Attribute(Name("txt"), "count"), Str("v"))),
          Call(Attribute(Name("txt"), "count"), Str("x"))),
        Call(Attribute(Name("txt"), "count"), Str("z"))))

  syntax Val ::= "solutionClosure" [function]
  rule solutionClosure => closureVal("txt", solutionBody, 0)

  // Branch oracle expressed with the reference semantics' occurrence counter.
  // The four codes are exactly the whitespace characters modeled by isWSC.
  syntax Int ::= whitespaceCount(IntSeq) [function]
  rule whitespaceCount(CS:IntSeq) =>
       cntSub(CS, iCons(32, .IntSeq))
    +Int cntSub(CS, iCons(9,  .IntSeq))
    +Int cntSub(CS, iCons(10, .IntSeq))
    +Int cntSub(CS, iCons(13, .IntSeq))

  syntax Int ::= commaCount(IntSeq) [function]
  rule commaCount(CS:IntSeq) => cntSub(CS, iCons(44, .IntSeq))

  // The zero-based odd alphabet positions are b,d,...,z.  The reference
  // cntSub function counts occurrences of each one-character string.
  syntax Int ::= oddAlphabetCount(IntSeq) [function]
  rule oddAlphabetCount(CS:IntSeq) =>
       cntSub(CS, iCons(98,  .IntSeq))
    +Int cntSub(CS, iCons(100, .IntSeq))
    +Int cntSub(CS, iCons(102, .IntSeq))
    +Int cntSub(CS, iCons(104, .IntSeq))
    +Int cntSub(CS, iCons(106, .IntSeq))
    +Int cntSub(CS, iCons(108, .IntSeq))
    +Int cntSub(CS, iCons(110, .IntSeq))
    +Int cntSub(CS, iCons(112, .IntSeq))
    +Int cntSub(CS, iCons(114, .IntSeq))
    +Int cntSub(CS, iCons(116, .IntSeq))
    +Int cntSub(CS, iCons(118, .IntSeq))
    +Int cntSub(CS, iCons(120, .IntSeq))
    +Int cntSub(CS, iCons(122, .IntSeq))
endmodule
