requires "semantic.k"

module SPEC-BODY-SENSITIVITY
  imports SEMANTIC

  // This is the real loop term with its subtraction constant materially
  // changed from Int(5) to Int(4), while retaining the original decodeSpec
  // obligation. For CS=cons(102,nil), actual code 98 differs from expected 97.
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
                BinOp("-", Call(Name("ord"), Name("ch")), Int(4)),
                Call(Name("ord"), Str("a"))),
              Int(26)),
            Call(Name("ord"), Str("a")))),
        CS:Chars) ~> KONT:K
      => VList(decodeSpec(CS)) ~> KONT
    </k>
    <ch> OLD:Int => OLD </ch>
  requires allLower(CS)
  [label(loop-wrong-body)]
endmodule
