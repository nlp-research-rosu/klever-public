requires "semantic.k"

module SPEC-BODY-MUTATION
  imports MPY-SEMANTICS

  claim [concatenate-loop]:
    <py>
      <k>
        loop("string", ITEMS:StrList,
          Assign(Name("result"),
            BinOp("+", Name("result"), Name("string"))))
        ~> (Return(Name("result")) .PyStmts) ~> cleanup
        => .K
      </k>
      <function> _FUN:Function => noFunction </function>
      <argument> lVal(_ALL:StrList) => lVal(.StrList) </argument>
      <accumulator> sVal(ACC:String) => sVal("") </accumulator>
      <iterationItem> sVal(_CURRENT:String) => sVal("") </iterationItem>
      <result> noResult => sVal(concatAcc(ACC, ITEMS)) </result>
    </py>

  // Actual executed body is changed: result starts at "!" while the original
  // postcondition is deliberately retained. Empty input is a false witness.
  claim [concatenate-correct-body-mutated]:
    <py>
      <k>
        load(Module(
          ImportFrom("typing", "List")
          FuncDef("concatenate", Params("strings"),
            Assign(Name("result"), Str("!"))
            For(Name("string"), Name("strings"),
              Assign(Name("result"),
                BinOp("+", Name("result"), Name("string"))))
            Return(Name("result")))))
        ~> invoke("concatenate", lVal(INPUT:StrList))
        => .K
      </k>
      <function> noFunction </function>
      <argument> lVal(.StrList) </argument>
      <accumulator> sVal("") </accumulator>
      <iterationItem> sVal("") </iterationItem>
      <result> noResult => sVal(concatAcc("", INPUT)) </result>
    </py>
endmodule
