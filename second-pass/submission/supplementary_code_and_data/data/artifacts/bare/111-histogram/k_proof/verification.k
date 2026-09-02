requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A closed constructor for the exact translated program. This avoids
  // copying a large AST into every claim while still proving solution.mpy.
  syntax Program ::= histogramProgram() [function, total]
  rule histogramProgram() =>
    Module(
      FuncDef("histogram", Params("test"),
        Assign(Name("letters"), Call(Attribute(Name("test"), "split"), .Exprs))
        Assign(Name("counts"), DictExpr(.Entries))
        Assign(Name("maximum"), Int(0))
        For(Name("letter"), Name("letters"),
          If(Compare(Name("letter"), CmpOp("in", Name("counts"))),
            Assign(Subscript(Name("counts"), Name("letter")),
                   BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1))),
            Assign(Subscript(Name("counts"), Name("letter")), Int(1)))
          If(Compare(Subscript(Name("counts"), Name("letter")),
                     CmpOp(">", Name("maximum"))),
            Assign(Name("maximum"), Subscript(Name("counts"), Name("letter"))),
            .Stmts))
        Assign(Name("result"), DictExpr(.Entries))
        For(Name("letter"), Name("counts"),
          If(Compare(Subscript(Name("counts"), Name("letter")),
                     CmpOp("==", Name("maximum"))),
            Assign(Subscript(Name("result"), Name("letter")),
                   Subscript(Name("counts"), Name("letter"))),
            .Stmts))
        Return(Name("result"))))

  // Denotational count pass. It is deliberately independent of exec/execFor:
  // each word increments its dictionary entry and raises the maximum if needed.
  syntax PyVal ::= nextCount(PyVal, PyVal) [function, total]
  rule nextCount(pyDict((WORD |-> VALUE:PyVal) REST, _), WORD)
    => addValues(VALUE, pyInt(1))
  rule nextCount(pyDict(DICT, _), WORD) => pyInt(1)
    requires notBool (WORD in_keys(DICT))
  rule nextCount(_, _) => pyInt(1) [owise]

  syntax Map ::= putCount(PyVal, Map) [function, total]
  rule putCount(WORD, ENV)
    => (ENV["letter" <- WORD])
       ["counts" <- dictSet(envGet(ENV, "counts"), WORD,
                            nextCount(envGet(ENV, "counts"), WORD))]

  syntax Map ::= raiseMaximum(PyVal, Map) [function, total]
  rule raiseMaximum(WORD, ENV)
    => ENV["maximum" <- dictGet(envGet(ENV, "counts"), WORD)]
    requires compareValues(">", dictGet(envGet(ENV, "counts"), WORD),
                                envGet(ENV, "maximum")) ==K pyBool(true)
  rule raiseMaximum(WORD, ENV) => ENV
    requires compareValues(">", dictGet(envGet(ENV, "counts"), WORD),
                                envGet(ENV, "maximum")) ==K pyBool(false)

  syntax Map ::= countIteration(PyVal, Map) [function, total]
  rule countIteration(WORD, ENV) => raiseMaximum(WORD, putCount(WORD, ENV))

  syntax Map ::= countLoop(List, Map) [function, total]
  rule countLoop(.List, ENV) => ENV
  rule countLoop(ListItem(WORD) (REST:List), ENV)
    => countLoop(REST, countIteration(WORD, ENV))

  // Denotational selection pass. The key list comes from the counted dict, and
  // only entries equal to the previously established maximum are retained.
  syntax Map ::= selectIteration(PyVal, Map) [function, total]
  rule selectIteration(WORD, ENV)
    => (ENV["letter" <- WORD])
       ["result" <- dictSet(envGet(ENV, "result"), WORD,
                            dictGet(envGet(ENV, "counts"), WORD))]
    requires compareValues("==", dictGet(envGet(ENV, "counts"), WORD),
                                 envGet(ENV, "maximum")) ==K pyBool(true)
  rule selectIteration(WORD, ENV) => ENV["letter" <- WORD]
    requires compareValues("==", dictGet(envGet(ENV, "counts"), WORD),
                                 envGet(ENV, "maximum")) ==K pyBool(false)

  syntax Map ::= selectLoop(List, Map) [function, total]
  rule selectLoop(.List, ENV) => ENV
  rule selectLoop(ListItem(WORD) (REST:List), ENV)
    => selectLoop(REST, selectIteration(WORD, ENV))

  syntax List ::= dictKeys(PyVal) [function, total]
  rule dictKeys(pyDict(_, KEYS)) => KEYS
  rule dictKeys(_) => .List [owise]

  syntax Map ::= initialEnvWith(List, PyVal) [function, total]
  rule initialEnvWith(WORDS, INPUT) =>
    "test" |-> INPUT
    "letters" |-> pyList(WORDS)
    "counts" |-> pyDict(.Map, .List)
    "maximum" |-> pyInt(0)

  syntax Map ::= initialEnv(List) [function, total]
  rule initialEnv(WORDS) => initialEnvWith(WORDS, pyWords(WORDS))

  syntax Map ::= afterCountWith(List, PyVal) [function, total]
  rule afterCountWith(WORDS, INPUT) => countLoop(WORDS, initialEnvWith(WORDS, INPUT))

  syntax Map ::= afterCount(List) [function, total]
  rule afterCount(WORDS) => afterCountWith(WORDS, pyWords(WORDS))

  syntax Map ::= beforeSelectWith(List, PyVal) [function, total]
  rule beforeSelectWith(WORDS, INPUT) =>
    afterCountWith(WORDS, INPUT)["result" <- pyDict(.Map, .List)]

  syntax Map ::= beforeSelect(List) [function, total]
  rule beforeSelect(WORDS) => beforeSelectWith(WORDS, pyWords(WORDS))

  syntax PyVal ::= histogramSpecWith(List, PyVal) [function, total]
  rule histogramSpecWith(WORDS, INPUT) =>
    envGet(selectLoop(iterable(envGet(afterCountWith(WORDS, INPUT), "counts")),
                      beforeSelectWith(WORDS, INPUT)),
           "result")

  syntax PyVal ::= histogramSpec(List) [function, total]
  rule histogramSpec(WORDS) => histogramSpecWith(WORDS, pyWords(WORDS))

  syntax PyVal ::= histogramSpecString(String) [function, total]
  rule histogramSpecString(INPUT) =>
    histogramSpecWith(splitWords(INPUT), pyString(INPUT))
endmodule
