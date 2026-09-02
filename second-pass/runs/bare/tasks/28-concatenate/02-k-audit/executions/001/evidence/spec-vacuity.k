requires "semantic.k"

module SPEC-VACUITY
  imports MPY-SEMANTICS

  // Fresh reviewer mutation.  The empty input really returns "", so requiring
  // "!" changes the result-bearing obligation to a reachable false target.
  claim [concatenate-false-empty]:
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
