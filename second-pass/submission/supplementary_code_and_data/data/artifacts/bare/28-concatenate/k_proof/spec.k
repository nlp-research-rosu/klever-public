requires "semantic.k"

module SPEC
  imports MPY-SEMANTICS

  // Loop invariant: starting with accumulator ACC and unconsumed ITEMS,
  // execution returns ACC followed by every remaining string.  The saved
  // values in the argument and iteration-variable cells are irrelevant to the
  // accumulator except when the loop body explicitly reads the current item.
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

  // End-to-end correctness of the exact constructor tree emitted in
  // solution.mpy, for an arbitrary finite list of strings.
  claim [concatenate-correct]:
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
