requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Opaque observations used only by symbolic execution.  Each observation is
  // introduced at the same K redex as the corresponding reference-semantics
  // operation, so repeated observations of the same input remain correlated.
  syntax Int ::= charCount(IntSeq, Int)
    [function, total, symbol(charCount), no-evaluators]
  syntax Int ::= headCode(IntSeq)
    [function, total, symbol(headCode), no-evaluators]
  syntax IntSeq ::= suffix4(IntSeq) [symbol(suffix4)]
  syntax Bool ::= suffixIs(IntSeq, Int)
    [function, total, symbol(suffixIs), no-evaluators]

  // The implementation only calls count with one-character strings.  This is
  // a proof abstraction of methods.k's cntSub(CS, iCons(C, .IntSeq)).
  rule <k> #applyK(
              toCall(boundMethodV(str(CS:IntSeq), "count")),
              (str(iCons(C:Int, .IntSeq)), .Vals))
        => charCount(CS, C) ... </k>
       [priority(40)]

  // This rule is reached only after the program has established length >= 5.
  // It abstracts subscript.k's concrete first-element projection.
  rule <k> Subscript(str(CS:IntSeq), 0)
        => str(iCons(headCode(CS), .IntSeq)) ... </k>
       requires isLen(CS) >=Int 5
       [priority(40)]

  // This names the value computed by the fixed [-4:] slice.  Concrete runs do
  // not import this module and therefore execute the full reference rule.
  rule <k> Subscript(
              str(CS:IntSeq),
              Slice(UnaryOp("-", Int(4)), NoBound, NoBound))
        => str(suffix4(CS)) ... </k>
       [priority(40)]

  // Correlate the three source-level equality tests without asking the
  // backend to decompose an opaque IntSeq projection.
  rule <k> Compare(
              str(suffix4(CS:IntSeq)),
              CmpOp("==",
                str(iCons(46, iCons(116, iCons(120, iCons(116, .IntSeq)))))))
        => suffixIs(CS, 0) ... </k>
       [priority(40)]
  rule <k> Compare(
              str(suffix4(CS:IntSeq)),
              CmpOp("==",
                str(iCons(46, iCons(101, iCons(120, iCons(101, .IntSeq)))))))
        => suffixIs(CS, 1) ... </k>
       [priority(40)]
  rule <k> Compare(
              str(suffix4(CS:IntSeq)),
              CmpOp("==",
                str(iCons(46, iCons(100, iCons(108, iCons(108, .IntSeq)))))))
        => suffixIs(CS, 2) ... </k>
       [priority(40)]

  syntax Bool ::= latinCode(Int) [function, total]
  rule latinCode(C:Int)
    => ((C >=Int 65 andBool C <=Int 90)
        orBool (C >=Int 97 andBool C <=Int 122))

  syntax Bool ::= allowedSuffix(IntSeq) [function, total]
  rule allowedSuffix(CS:IntSeq)
    => suffixIs(CS, 0) orBool suffixIs(CS, 1) orBool suffixIs(CS, 2)

  syntax Int ::= digitCount(IntSeq) [function, total]
  rule digitCount(CS:IntSeq)
    => charCount(CS, 48) +Int charCount(CS, 49)
       +Int charCount(CS, 50) +Int charCount(CS, 51)
       +Int charCount(CS, 52) +Int charCount(CS, 53)
       +Int charCount(CS, 54) +Int charCount(CS, 55)
       +Int charCount(CS, 56) +Int charCount(CS, 57)

  // This is exactly solution.mpy, named as a function so it is auditable
  // against the generated artifact.
  syntax Module ::= "solutionModule" [function]
  rule solutionModule =>
    Module(
      FuncDef("file_name_check", Params("file_name"),
        Expr(
          Str(
            "Return \"Yes\" exactly when file_name satisfies the prompt's rules."))
        If(Compare(
          Call(Attribute(Name("file_name"), "count"), Str(".")),
          CmpOp("!=", Int(1))),
          Return(Str("No")),
          .Stmts)
        If(Compare(Call(Name("len"), Name("file_name")), CmpOp("<", Int(5))),
          Return(Str("No")),
          .Stmts)
        Assign(
          Name("first_code"),
          Call(Name("ord"), Subscript(Name("file_name"), Int(0))))
        If(UnaryOp(
          "not",
          BoolOp(
            "or",
            BoolOp(
              "and",
              Compare(Name("first_code"), CmpOp(">=", Int(65))),
              Compare(Name("first_code"), CmpOp("<=", Int(90)))),
            BoolOp(
              "and",
              Compare(Name("first_code"), CmpOp(">=", Int(97))),
              Compare(Name("first_code"), CmpOp("<=", Int(122)))))),
          Return(Str("No")),
          .Stmts)
        Assign(
          Name("suffix"),
          Subscript(
            Name("file_name"),
            Slice(UnaryOp("-", Int(4)), NoBound, NoBound)))
        If(UnaryOp(
          "not",
          BoolOp(
            "or",
            Compare(Name("suffix"), CmpOp("==", Str(".txt"))),
            Compare(Name("suffix"), CmpOp("==", Str(".exe"))),
            Compare(Name("suffix"), CmpOp("==", Str(".dll"))))),
          Return(Str("No")),
          .Stmts)
        Assign(
          Name("digit_count"),
          BinOp(
            "+",
            BinOp(
              "+",
              BinOp(
                "+",
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      BinOp(
                        "+",
                        BinOp(
                          "+",
                          BinOp(
                            "+",
                            Call(
                              Attribute(Name("file_name"), "count"),
                              Str("0")),
                            Call(
                              Attribute(Name("file_name"), "count"),
                              Str("1"))),
                          Call(
                            Attribute(Name("file_name"), "count"),
                            Str("2"))),
                        Call(
                          Attribute(Name("file_name"), "count"),
                          Str("3"))),
                      Call(Attribute(Name("file_name"), "count"), Str("4"))),
                    Call(Attribute(Name("file_name"), "count"), Str("5"))),
                  Call(Attribute(Name("file_name"), "count"), Str("6"))),
                Call(Attribute(Name("file_name"), "count"), Str("7"))),
              Call(Attribute(Name("file_name"), "count"), Str("8"))),
            Call(Attribute(Name("file_name"), "count"), Str("9"))))
        If(Compare(Name("digit_count"), CmpOp(">", Int(3))),
          Return(Str("No")),
          .Stmts)
        Return(Str("Yes"))))

  syntax Stmts ::= moduleBody(Module) [function]
  rule moduleBody(
         Module(FuncDef(_F:String, Params(_PNS:ParamNames), BODY:Stmts)))
    => BODY

  syntax KItem ::= runFileNameCheck(IntSeq)
  rule <k> runFileNameCheck(CS:IntSeq)
        => #applyK(
             toCall(closureVal(
               ("file_name", .ParamNames), moduleBody(solutionModule), 0)),
             (str(CS), .Vals)) ... </k>
endmodule
