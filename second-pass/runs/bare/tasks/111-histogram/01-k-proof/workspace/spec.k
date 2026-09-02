requires "verification.k"
requires "lemmas.k"

module COUNT-LOOP-SPEC
  imports VERIFICATION

  claim [count-empty]:
    <k>
      execFor(Name("letter"), .List,
        If(Compare(Name("letter"), CmpOp("in", Name("counts"))),
          Assign(Subscript(Name("counts"), Name("letter")),
                 BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1))),
          Assign(Subscript(Name("counts"), Name("letter")), Int(1)))
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp(">", Name("maximum"))),
          Assign(Name("maximum"), Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ENV:Map)
      => normal(ENV)
    </k>

  claim [count-existing-raises-step]:
    <k>
      execFor(Name("letter"), ListItem(WORD:PyVal),
        If(Compare(Name("letter"), CmpOp("in", Name("counts"))),
          Assign(Subscript(Name("counts"), Name("letter")),
                 BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1))),
          Assign(Subscript(Name("counts"), Name("letter")), Int(1)))
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp(">", Name("maximum"))),
          Assign(Name("maximum"), Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ("counts" |-> pyDict((WORD |-> pyInt(N:Int)) DICTREST:Map, KEYS:List)
         "maximum" |-> pyInt(M:Int)
         ENVREST:Map))
      => normal(countIteration(WORD,
           ("counts" |-> pyDict((WORD |-> pyInt(N)) DICTREST, KEYS)
            "maximum" |-> pyInt(M)
            ENVREST)))
    </k>
    requires N +Int 1 >Int M

  claim [count-fresh-step]:
    <k>
      execFor(Name("letter"), ListItem(WORD:PyVal),
        If(Compare(Name("letter"), CmpOp("in", Name("counts"))),
          Assign(Subscript(Name("counts"), Name("letter")),
                 BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1))),
          Assign(Subscript(Name("counts"), Name("letter")), Int(1)))
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp(">", Name("maximum"))),
          Assign(Name("maximum"), Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ("counts" |-> pyDict(DICT:Map, KEYS:List)
         "maximum" |-> pyInt(M:Int)
         ENVREST:Map))
      => normal(countIteration(WORD,
           ("counts" |-> pyDict(DICT, KEYS)
            "maximum" |-> pyInt(M)
            ENVREST)))
    </k>
    requires notBool (WORD in_keys(DICT)) andBool 1 >Int M

  claim [count-existing-keeps-step]:
    <k>
      execFor(Name("letter"), ListItem(WORD:PyVal),
        If(Compare(Name("letter"), CmpOp("in", Name("counts"))),
          Assign(Subscript(Name("counts"), Name("letter")),
                 BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1))),
          Assign(Subscript(Name("counts"), Name("letter")), Int(1)))
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp(">", Name("maximum"))),
          Assign(Name("maximum"), Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ("counts" |-> pyDict((WORD |-> pyInt(N:Int)) DICTREST:Map, KEYS:List)
         "maximum" |-> pyInt(M:Int)
         ENVREST:Map))
      => normal(countIteration(WORD,
           ("counts" |-> pyDict((WORD |-> pyInt(N)) DICTREST, KEYS)
            "maximum" |-> pyInt(M)
            ENVREST)))
    </k>
    requires N +Int 1 <=Int M

  claim [count-fresh-keeps-step]:
    <k>
      execFor(Name("letter"), ListItem(WORD:PyVal),
        If(Compare(Name("letter"), CmpOp("in", Name("counts"))),
          Assign(Subscript(Name("counts"), Name("letter")),
                 BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1))),
          Assign(Subscript(Name("counts"), Name("letter")), Int(1)))
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp(">", Name("maximum"))),
          Assign(Name("maximum"), Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ("counts" |-> pyDict(DICT:Map, KEYS:List)
         "maximum" |-> pyInt(M:Int)
         ENVREST:Map))
      => normal(countIteration(WORD,
           ("counts" |-> pyDict(DICT, KEYS)
            "maximum" |-> pyInt(M)
            ENVREST)))
    </k>
    requires notBool (WORD in_keys(DICT)) andBool 1 <=Int M
endmodule

module MAIN-CORRECTNESS-SPEC
  imports VERIFIED-LOOP-LEMMAS

  claim [all-token-lists]:
    <k>
      executeWords(histogramProgram(), WORDS:List)
      => histogramSpec(WORDS)
    </k>

  claim [all-space-separated-strings]:
    <k>
      execute(histogramProgram(), INPUT:String)
      => histogramSpecString(INPUT)
    </k>
endmodule

module SELECT-LOOP-SPEC
  imports VERIFICATION

  claim [select-empty]:
    <k>
      execFor(Name("letter"), .List,
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp("==", Name("maximum"))),
          Assign(Subscript(Name("result"), Name("letter")),
                 Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ENV:Map)
      => normal(ENV)
    </k>

  claim [select-equal-step]:
    <k>
      execFor(Name("letter"), ListItem(WORD:PyVal),
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp("==", Name("maximum"))),
          Assign(Subscript(Name("result"), Name("letter")),
                 Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ("counts" |-> pyDict((WORD |-> VALUE:PyVal) DICTREST:Map, COUNTKEYS:List)
         "maximum" |-> VALUE
         "result" |-> pyDict(RESULTDICT:Map, RESULTKEYS:List)
         ENVREST:Map))
      => normal(selectIteration(WORD,
           ("counts" |-> pyDict((WORD |-> VALUE) DICTREST, COUNTKEYS)
            "maximum" |-> VALUE
            "result" |-> pyDict(RESULTDICT, RESULTKEYS)
            ENVREST)))
    </k>

  claim [select-unequal-step]:
    <k>
      execFor(Name("letter"), ListItem(WORD:PyVal),
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp("==", Name("maximum"))),
          Assign(Subscript(Name("result"), Name("letter")),
                 Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ("counts" |-> pyDict((WORD |-> VALUE:PyVal) DICTREST:Map, COUNTKEYS:List)
         "maximum" |-> MAXIMUM:PyVal
         "result" |-> pyDict(RESULTDICT:Map, RESULTKEYS:List)
         ENVREST:Map))
      => normal(selectIteration(WORD,
           ("counts" |-> pyDict((WORD |-> VALUE) DICTREST, COUNTKEYS)
            "maximum" |-> MAXIMUM
            "result" |-> pyDict(RESULTDICT, RESULTKEYS)
            ENVREST)))
    </k>
    requires VALUE =/=K MAXIMUM
endmodule

module EXAMPLES-SPEC
  imports VERIFICATION

  claim [example-all-once]:
    <k>
      execute(histogramProgram(), "a b c")
      => pyDict(
           pyString("a") |-> pyInt(1)
           pyString("b") |-> pyInt(1)
           pyString("c") |-> pyInt(1),
           ListItem(pyString("a"))
           ListItem(pyString("b"))
           ListItem(pyString("c")))
    </k>

  claim [example-tied-two]:
    <k>
      execute(histogramProgram(), "a b b a")
      => pyDict(
           pyString("a") |-> pyInt(2)
           pyString("b") |-> pyInt(2),
           ListItem(pyString("a"))
           ListItem(pyString("b")))
    </k>

  claim [example-filter-one]:
    <k>
      execute(histogramProgram(), "a b c a b")
      => pyDict(
           pyString("a") |-> pyInt(2)
           pyString("b") |-> pyInt(2),
           ListItem(pyString("a"))
           ListItem(pyString("b")))
    </k>

  claim [example-single-winner]:
    <k>
      execute(histogramProgram(), "b b b b a")
      => pyDict(pyString("b") |-> pyInt(4),
                ListItem(pyString("b")))
    </k>

  claim [example-empty]:
    <k>
      execute(histogramProgram(), "")
      => pyDict(.Map, .List)
    </k>
endmodule
