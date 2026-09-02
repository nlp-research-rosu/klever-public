requires "semantic.k"

module SPEC-VACUITY-AUDIT
  imports MPY-SEMANTICS

  // Fresh false result mutation. The entry precondition is the ordinary
  // initialized configuration with INPUT = []; Python and the K semantics both
  // return "", while this destination demands "!".
  claim [empty-input-wrong-result]:
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
        ~> invoke("concatenate", lVal(.StrList))
        => .K
      </k>
      <function> noFunction </function>
      <argument> lVal(.StrList) </argument>
      <accumulator> sVal("") </accumulator>
      <iterationItem> sVal("") </iterationItem>
      <result> noResult => sVal("!") </result>
    </py>
endmodule
