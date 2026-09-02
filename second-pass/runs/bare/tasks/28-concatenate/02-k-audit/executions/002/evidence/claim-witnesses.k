requires "semantic.k"

module CLAIM-WITNESSES
  imports MPY-SEMANTICS

  // Ground instance of the loop claim:
  // ACC = "a", ITEMS = ["b", "c"], ALL = [], CURRENT = "".
  claim [ground-loop-witness]:
    <py>
      <k>
        loop("string", "b" :: "c" :: .StrList,
          Assign(Name("result"),
            BinOp("+", Name("result"), Name("string"))))
        ~> (Return(Name("result")) .PyStmts) ~> cleanup
        => .K
      </k>
      <function> noFunction => noFunction </function>
      <argument> lVal(.StrList) => lVal(.StrList) </argument>
      <accumulator> sVal("a") => sVal("") </accumulator>
      <iterationItem> sVal("") => sVal("") </iterationItem>
      <result> noResult => sVal("abc") </result>
    </py>

  // Ground instance of the entry claim with the prompt's nonempty example.
  claim [ground-entry-witness]:
    <py>
      <k>
        load(Module(
          ImportFrom("typing", "List")
          FuncDef("concatenate", Params("strings"),
            Assign(Name("result"), Str(""))
            For(Name("string"), Name("strings"),
              Assign(Name("result"),
                BinOp("+", Name("result"), Name("string"))))
            Return(Name("result")))))
        ~> invoke("concatenate",
             lVal("a" :: "b" :: "c" :: .StrList))
        => .K
      </k>
      <function> noFunction </function>
      <argument> lVal(.StrList) </argument>
      <accumulator> sVal("") </accumulator>
      <iterationItem> sVal("") </iterationItem>
      <result> noResult => sVal("abc") </result>
    </py>
endmodule
