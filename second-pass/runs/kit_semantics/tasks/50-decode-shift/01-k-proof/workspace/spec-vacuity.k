requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [character-inverse]:
    <k> decodeCode(encodeCode(C:Int)) => C </k>
    requires 97 <=Int C andBool C <=Int 122

  claim [loop-invariant]:
    <k>
      #loop(
        str(CS:IntSeq),
        Name("ch"),
        Assign(
          Name("result"),
          BinOp(
            "+",
            Name("result"),
            Call(
              Name("chr"),
              BinOp(
                "+",
                BinOp(
                  "%",
                  BinOp(
                    "-",
                    BinOp("-", Call(Name("ord"), Name("ch")), Int(5)),
                    Call(Name("ord"), Str("a"))),
                  Int(26)),
                Call(Name("ord"), Str("a"))))))
        .Stmts)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "s" |-> str(INPUT:IntSeq)
        ("result" |-> (str(ACC:IntSeq) => str(decodeAcc(CS, ACC))))
        ("ch" |-> (CH:Val => ?CH:Val)),
        parent(0))
      0 |-> scope(
        "decode_shift" |->
          closureVal(
            "s",
            Expr(Str("\n    takes as input string encoded with encode_shift function. Returns decoded string.\n    "))
            Assign(Name("result"), Str(""))
            Assign(Name("ch"), Str(""))
            For(
              Name("ch"),
              Name("s"),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  Name("result"),
                  Call(
                    Name("chr"),
                    BinOp(
                      "+",
                      BinOp(
                        "%",
                        BinOp(
                          "-",
                          BinOp("-", Call(Name("ord"), Name("ch")), Int(5)),
                          Call(Name("ord"), Str("a"))),
                        Int(26)),
                      Call(Name("ord"), Str("a"))))))
              .Stmts)
            Return(Name("result"))
            .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    requires lowerCodes(CS)

  claim [decode-shift]:
    <k>
      Call(Name("decode_shift"), str(CS:IntSeq))
      => str(seqConcat(decodeAcc(CS, .IntSeq), iCons(97, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "decode_shift" |->
          closureVal(
            "s",
            Expr(Str("\n    takes as input string encoded with encode_shift function. Returns decoded string.\n    "))
            Assign(Name("result"), Str(""))
            Assign(Name("ch"), Str(""))
            For(
              Name("ch"),
              Name("s"),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  Name("result"),
                  Call(
                    Name("chr"),
                    BinOp(
                      "+",
                      BinOp(
                        "%",
                        BinOp(
                          "-",
                          BinOp("-", Call(Name("ord"), Name("ch")), Int(5)),
                          Call(Name("ord"), Str("a"))),
                        Int(26)),
                      Call(Name("ord"), Str("a"))))))
              .Stmts)
            Return(Name("result"))
            .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires lowerCodes(CS)
endmodule
