requires "program-generated.k"

module VERIFICATION
  imports PROGRAM-GENERATED

  // Derived directly from MPY-STR's complete lexicographic cases: for two
  // one-character strings, lexicographic order is integer-code order.
  rule strLt(
         iCons(C:Int, .IntSeq),
         iCons(D:Int, .IntSeq))
    => C <Int D
    [simplification]

  // Exact AST aliases for the translated implementation.  These construct
  // syntax only; they do not summarize or replace execution.
  syntax Stmts ::= antiInnerBody() [function, total]
                 | antiPostInsert() [function, total]
                 | antiOuterBody() [function, total]
                 | antiTail() [function, total]

  rule antiInnerBody()
    => If(
         BoolOp(
           "and",
           (UnaryOp("not", Name("inserted")),
            Compare(Name("char"), CmpOp("<", Name("old_char"))),
            .Exprs)),
         AugAssign(Name("new_word"), "+", Name("char"))
         Assign(Name("inserted"), Bool(true))
         .Stmts,
         .Stmts)
       AugAssign(Name("new_word"), "+", Name("old_char"))
       .Stmts

  rule antiPostInsert()
    => If(
         UnaryOp("not", Name("inserted")),
         AugAssign(Name("new_word"), "+", Name("char"))
         Assign(Name("inserted"), Bool(true))
         .Stmts,
         .Stmts)
       Assign(Name("word"), Name("new_word"))
       .Stmts

  rule antiOuterBody()
    => If(
         Compare(Name("char"), CmpOp("==", Str(" "))),
         AugAssign(Name("result"), "+", Name("word"))
         AugAssign(Name("result"), "+", Str(" "))
         Assign(Name("word"), Str(""))
         .Stmts,
         Assign(Name("new_word"), Str(""))
         Assign(Name("inserted"), Bool(false))
         For(Name("old_char"), Name("word"), antiInnerBody())
         antiPostInsert())
       .Stmts

  rule antiTail()
    => AugAssign(Name("result"), "+", Name("word"))
       Return(Name("result"))
       .Stmts

  // Exact value produced by the insertion loop from its loop-head state.
  // The guard-free constructor equations unfold one step without splitting an
  // unknown tail.
  syntax IntSeq ::= insertGo(IntSeq, Int, IntSeq, Bool)
                    [function, total]
  rule insertGo(.IntSeq, C:Int, A:IntSeq, B:Bool)
    => #if B
       #then A
       #else seqConcat(A, iCons(C, .IntSeq))
       #fi
  rule insertGo(
         iCons(OLD:Int, IS:IntSeq),
         C:Int,
         A:IntSeq,
         B:Bool)
    => #if notBool B andBool C <Int OLD
       #then insertGo(
               IS,
               C,
               seqConcat(
                 seqConcat(A, iCons(C, .IntSeq)),
                 iCons(OLD, .IntSeq)),
               true)
       #else insertGo(
               IS,
               C,
               seqConcat(A, iCons(OLD, .IntSeq)),
               B)
       #fi

  // Exact value produced by the outer loop and its function tail.
  syntax IntSeq ::= antiGo(IntSeq, IntSeq, IntSeq) [function, total]
  rule antiGo(.IntSeq, R:IntSeq, W:IntSeq)
    => seqConcat(R, W)
  rule antiGo(iCons(C:Int, S:IntSeq), R:IntSeq, W:IntSeq)
    => #if C ==Int 32
       #then antiGo(
               S,
               seqConcat(seqConcat(R, W), iCons(32, .IntSeq)),
               .IntSeq)
       #else antiGo(
               S,
               R,
               insertGo(W, C, .IntSeq, false))
       #fi

endmodule
