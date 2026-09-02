requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Parse-time alias for the exact body generated in solution.mpy.  This macro
  // disappears before execution; every operation below executes in MPY.
  syntax Stmts ::= "fileNameCheckBody" [macro]
  rule fileNameCheckBody
    => If(
         Compare(
           Call(Attribute(Name("file_name"), "count"), Str(".")),
           CmpOp("!=", Int(1))),
         Return(Str("No")),
         .Stmts)
       If(
         Compare(
           Subscript(Name("file_name"), Int(0)),
           CmpOp(
             "not in",
             Str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))),
         Return(Str("No")),
         .Stmts)
       If(
         UnaryOp(
           "not",
           BoolOp(
             "or",
             Compare(
               Subscript(
                 Name("file_name"),
                 Slice(UnaryOp("-", Int(4)), NoBound, NoBound)),
               CmpOp("==", Str(".txt"))),
             Compare(
               Subscript(
                 Name("file_name"),
                 Slice(UnaryOp("-", Int(4)), NoBound, NoBound)),
               CmpOp("==", Str(".exe"))),
             Compare(
               Subscript(
                 Name("file_name"),
                 Slice(UnaryOp("-", Int(4)), NoBound, NoBound)),
               CmpOp("==", Str(".dll"))))),
         Return(Str("No")),
         .Stmts)
       If(
         Compare(
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
                       Call(
                         Attribute(Name("file_name"), "count"),
                         Str("4"))),
                     Call(
                       Attribute(Name("file_name"), "count"),
                       Str("5"))),
                   Call(
                     Attribute(Name("file_name"), "count"),
                     Str("6"))),
                 Call(
                   Attribute(Name("file_name"), "count"),
                   Str("7"))),
               Call(
                 Attribute(Name("file_name"), "count"),
                 Str("8"))),
             Call(
               Attribute(Name("file_name"), "count"),
               Str("9"))),
           CmpOp(">", Int(3))),
         Return(Str("No")),
         .Stmts)
       Return(Str("Yes"))

  // Mathematical summaries used only to state the claim partitions.
  syntax Int ::= decimalDigitCount(IntSeq) [function, total]
  rule decimalDigitCount(CS)
    => cntSub(CS, strToCodes("0"))
       +Int cntSub(CS, strToCodes("1"))
       +Int cntSub(CS, strToCodes("2"))
       +Int cntSub(CS, strToCodes("3"))
       +Int cntSub(CS, strToCodes("4"))
       +Int cntSub(CS, strToCodes("5"))
       +Int cntSub(CS, strToCodes("6"))
       +Int cntSub(CS, strToCodes("7"))
       +Int cntSub(CS, strToCodes("8"))
       +Int cntSub(CS, strToCodes("9"))

  syntax Bool ::= fileExtensionIs(IntSeq, IntSeq) [function, total]
  rule fileExtensionIs(CS, EXT)
    => applyCmp(
         "==",
         doSlice(str(CS), someB(-4), noB, noB),
         str(EXT))

  syntax Bool ::= allowedFileExtension(IntSeq) [function, total]
  rule allowedFileExtension(CS)
    => fileExtensionIs(CS, strToCodes(".txt"))
       orBool fileExtensionIs(CS, strToCodes(".exe"))
       orBool fileExtensionIs(CS, strToCodes(".dll"))

  rule N:Int >Int 3 => false
    requires N <=Int 3
    [simplification]

endmodule
