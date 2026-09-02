requires "semantic.k"

module SPEC-VACUITY
  imports SEMANTIC

  claim <k> decodeCode(encodeCode(C:Int)) => C ...</k>
    requires isLowerCode(C)
  [label(code-inverse)]

  claim
    <k>
      comp("ch",
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
            Call(Name("ord"), Str("a")))),
        CS:Chars) ~> KONT:K
      => VList(decodeSpec(CS)) ~> KONT
    </k>
    <ch> OLD:Int => OLD </ch>
  requires allLower(CS)
  [label(loop-correct)]

  // Fresh false mutation: the real program decodes, but this result obligation
  // demands encoding. For CS=cons(102,nil), execution returns code 97 while
  // encodeSpec returns code 107.
  claim
      <k>
        Module(
          FuncDef("decode_shift", Params("s"),
            Return(
              Call(
                Attribute(Str(""), "join"),
                ListComp(Call(
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
                    Call(Name("ord"), Str("a")))),
                  CompFor(Name("ch"), Name("s"), Bool(true)))))))
        => .K
      </k>
      <s> nil => CS </s>
      <ch> 0 => 0 </ch>
      <input> CS:Chars => CS </input>
      <result> .K => VChars(encodeSpec(CS)) </result>
  requires allLower(CS)
  [label(program-wrong-result)]
endmodule
