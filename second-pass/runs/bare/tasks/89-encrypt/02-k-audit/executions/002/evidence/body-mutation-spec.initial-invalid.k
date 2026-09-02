requires "semantic.k"

module BODY-MUTATION-SPEC
  imports MPY

  claim [shift-five-is-not-shift-four]:
    <k>
      Module(
        FuncDef("encrypt", Params("s"),
          If(Compare(Name("s"), CmpOp("==", Str(""))),
             Return(Str("")),
             .Stmts)
          Return(
            BinOp("+",
              Call(Name("chr"),
                BinOp("+",
                  BinOp("%",
                    BinOp("+",
                      BinOp("-",
                        Call(Name("ord"), Subscript(Name("s"), Int(0))),
                        Int(97)),
                      Int(5)),
                    Int(26)),
                  Int(97))),
              Call(Name("encrypt"),
                Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)))))))
      ~> start("a")
      => .K
    </k>
    <function>
      <funName> "" => "encrypt" </funName>
      <parameter> "" => "s" </parameter>
      <body>
        .Stmts
        =>
        If(Compare(Name("s"), CmpOp("==", Str(""))),
           Return(Str("")),
           .Stmts)
        Return(
          BinOp("+",
            Call(Name("chr"),
              BinOp("+",
                BinOp("%",
                  BinOp("+",
                    BinOp("-",
                      Call(Name("ord"), Subscript(Name("s"), Int(0))),
                      Int(97)),
                    Int(5)),
                  Int(26)),
                Int(97))),
            Call(Name("encrypt"),
              Subscript(Name("s"), Slice(Int(1), NoBound, NoBound))))))
      </body>
    </function>
    <env> .Map </env>
    <stack> .List </stack>
    <result> noResult => "e" </result>
endmodule
