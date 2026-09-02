requires "semantic.k"

module SPEC
  imports SEMANTIC

  // The arithmetic used by decode_shift is the inverse of the prompt's
  // encode_shift arithmetic for every lowercase character code.
  claim <k> decodeCode(encodeCode(C:Int)) => C ...</k>
    requires isLowerCode(C)
  [label(code-inverse)]

  // Loop invariant for the translated comprehension. The environment is
  // restored after each character, so the invariant composes inductively.
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

  // For every lowercase input string, execution of the translated solution
  // returns the independently specified per-character Caesar decoding.
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
      <result> .K => VChars(decodeSpec(CS)) </result>
  requires allLower(CS)
  [label(program-correct)]
endmodule
