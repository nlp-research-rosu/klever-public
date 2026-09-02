requires "semantic.k"

module COUNT-UPPER-VERIFICATION
  imports MPY-SEMANTIC

  syntax Program ::= "countUpperProgram" [function]

  rule countUpperProgram
    => Module(
         FuncDef("count_upper", Params("s"),
           If(
             Compare(
               Call(Name("len"), Name("s")),
               CmpOp("==", Int(0))
             ),
             Return(Int(0)),
             .Stmts
           )
           If(
             Compare(
               Subscript(Name("s"), Int(0)),
               CmpOp("in", Str("AEIOU"))
             ),
             Return(
               BinOp(
                 "+",
                 Int(2),
                 Call(
                   Name("count_upper"),
                   Subscript(
                     Name("s"),
                     Slice(Int(2), NoBound, NoBound)
                   )
                 )
               )
             ),
             .Stmts
           )
           Return(
             Call(
               Name("count_upper"),
               Subscript(
                 Name("s"),
                 Slice(Int(2), NoBound, NoBound)
               )
             )
           )
         )
       )

  // Mathematical reference function: inspect the first character, then drop
  // two characters.  Thus each recursive position is exactly an even index of
  // the original string.
  syntax Int ::= countUpperSpec(String) [function, total]
  syntax String ::= dropTwo(String) [function]

  rule countUpperSpec(S) => 0
    requires lengthString(S) ==Int 0
  rule countUpperSpec(S)
    => 1 +Int countUpperSpec(dropTwo(S))
    requires lengthString(S) =/=Int 0
     andBool substrString(S, 0, 1) ==String "A"
  rule countUpperSpec(S)
    => 1 +Int countUpperSpec(dropTwo(S))
    requires lengthString(S) =/=Int 0
     andBool substrString(S, 0, 1) ==String "E"
  rule countUpperSpec(S)
    => 1 +Int countUpperSpec(dropTwo(S))
    requires lengthString(S) =/=Int 0
     andBool substrString(S, 0, 1) ==String "I"
  rule countUpperSpec(S)
    => 1 +Int countUpperSpec(dropTwo(S))
    requires lengthString(S) =/=Int 0
     andBool substrString(S, 0, 1) ==String "O"
  rule countUpperSpec(S)
    => 1 +Int countUpperSpec(dropTwo(S))
    requires lengthString(S) =/=Int 0
     andBool substrString(S, 0, 1) ==String "U"
  // If neither the empty case nor a vowel case applies, the first character
  // contributes zero. `owise` is the logical complement of the cases above.
  rule countUpperSpec(S) => countUpperSpec(dropTwo(S)) [owise]

  rule dropTwo(S)
    => substrString(S, minInt(2, lengthString(S)), lengthString(S))

endmodule
