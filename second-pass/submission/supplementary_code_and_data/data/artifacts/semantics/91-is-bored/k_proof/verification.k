requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Names for the exact translated source fragments.  These are merely AST
  // abbreviations; their equations do not summarize any execution.
  syntax Stmts ::= "boredLoopBody" [function, total]
                 | "boredFunctionBody" [function, total]

  rule boredLoopBody
    => Assign(Name("code"), Call(Name("ord"), Name("ch")))
       If(
         BoolOp(
           "or",
           Compare(Name("code"), CmpOp("==", Int(46))),
           Compare(Name("code"), CmpOp("==", Int(63))),
           Compare(Name("code"), CmpOp("==", Int(33)))
         ),
         Assign(Name("state"), Int(0)),
         If(
           Compare(Name("state"), CmpOp("==", Int(0))),
           If(
             BoolOp(
               "or",
               Compare(Name("code"), CmpOp("==", Int(32))),
               BoolOp(
                 "and",
                 Compare(Name("code"), CmpOp(">=", Int(9))),
                 Compare(Name("code"), CmpOp("<=", Int(13)))
               )
             ),
             Assign(Name("state"), Int(0)),
             If(
               Compare(Name("code"), CmpOp("==", Int(73))),
               Assign(Name("state"), Int(1)),
               Assign(Name("state"), Int(2))
             )
           ),
           If(
             Compare(Name("state"), CmpOp("==", Int(1))),
             If(
               Compare(Name("code"), CmpOp("==", Int(32))),
               AugAssign(Name("count"), "+", Int(1)),
               .Stmts
             )
             Assign(Name("state"), Int(2)),
             .Stmts
           )
         )
       )

  rule boredFunctionBody
    => Assign(Name("count"), Int(0))
       Assign(Name("state"), Int(0))
       Assign(Name("ch"), Str(""))
       Assign(Name("code"), Int(0))
       For(Name("ch"), Name("S"), boredLoopBody)
       Return(Name("count"))

  // The three scanner states have the following contract:
  //   0: only leading whitespace has been seen in the current sentence;
  //   1: that first non-whitespace character was "I";
  //   2: the sentence can no longer be a boredom.
  syntax Bool ::= isBoredDelimiter(Int) [function, total]
                | isBoredWhitespace(Int) [function, total]

  rule isBoredDelimiter(C:Int)
    => C ==Int 46 orBool C ==Int 63 orBool C ==Int 33

  rule isBoredWhitespace(C:Int)
    => C ==Int 32 orBool (C >=Int 9 andBool C <=Int 13)

  // bored0/bored1/bored2 are an independent recursive specification over
  // character codes.  The Int argument is the count accumulated so far.
  syntax Val ::= bored0(IntSeq, Int) [function, total, no-evaluators]
               | bored1(IntSeq, Int) [function, total, no-evaluators]
               | bored2(IntSeq, Int) [function, total, no-evaluators]

  rule bored0(.IntSeq, N:Int) => N [simplification]
  rule bored0(iCons(C:Int, R:IntSeq), N:Int)
    => #if isBoredDelimiter(C)
       #then bored0(R, N)
       #else #if isBoredWhitespace(C)
             #then bored0(R, N)
             #else #if C ==Int 73
                   #then bored1(R, N)
                   #else bored2(R, N)
                   #fi
             #fi
       #fi
    [simplification]

  rule bored1(.IntSeq, N:Int) => N [simplification]
  rule bored1(iCons(C:Int, R:IntSeq), N:Int)
    => #if isBoredDelimiter(C)
       #then bored0(R, N)
       #else #if C ==Int 32
             #then bored2(R, N +Int 1)
             #else bored2(R, N)
             #fi
       #fi
    [simplification]

  rule bored2(.IntSeq, N:Int) => N [simplification]
  rule bored2(iCons(C:Int, R:IntSeq), N:Int)
    => #if isBoredDelimiter(C)
       #then bored0(R, N)
       #else bored2(R, N)
       #fi
    [simplification]
endmodule
