requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY
  imports INT

  syntax Stmts ::= "parseMusicBody" [function, total]
                 | "parseMusicCharBody" [function, total]
                 | "mutatedParseMusicBody" [function, total]
                 | "mutatedParseMusicCharBody" [function, total]

  // Exact mathematical state transition performed for one input character.
  syntax Int ::= nextCurrent(Int, Int) [function, total]
  syntax ValSeq ::= nextResult(ValSeq, Int, Int) [function, total]

  // Exact fold of those transitions over the unprocessed character codes.
  syntax Int ::= scanCurrent(IntSeq, Int) [function, total]
  syntax ValSeq ::= scanResult(IntSeq, Int, ValSeq) [function, total]
                  | musicResult(IntSeq) [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY
  imports INT
  imports BOOL

  rule parseMusicBody =>
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("current"), Int(0))
    For(Name("char"), Name("music_string"), parseMusicCharBody)
    If(Compare(Name("current"), CmpOp("==", Int(4))),
       Expr(Call(Attribute(Name("result"), "append"), Name("current") , .Exprs)) .Stmts,
       .Stmts)
    Return(Name("result"))

  rule parseMusicCharBody =>
    If(Compare(Name("char"), CmpOp("==", Str("o"))),
       Assign(Name("current"), Int(4)) .Stmts,
       If(Compare(Name("char"), CmpOp("==", Str("."))),
          Assign(Name("current"), Int(1)) .Stmts,
          If(Compare(Name("char"), CmpOp("==", Str("|"))),
             If(Compare(Name("current"), CmpOp("==", Int(4))),
                Assign(Name("current"), Int(2)) .Stmts,
                .Stmts)
             Expr(Call(Attribute(Name("result"), "append"), Name("current") , .Exprs))
             Assign(Name("current"), Int(0)),
             If(Compare(Name("current"), CmpOp("==", Int(4))),
                Expr(Call(Attribute(Name("result"), "append"), Name("current") , .Exprs)) .Stmts,
                .Stmts)
             Assign(Name("current"), Int(0)))))

  // Validation-only body mutation; no positive proof claim references it.
  rule mutatedParseMusicBody =>
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("current"), Int(0))
    For(Name("char"), Name("music_string"), mutatedParseMusicCharBody)
    If(Compare(Name("current"), CmpOp("==", Int(4))),
       Expr(Call(Attribute(Name("result"), "append"), Name("current") , .Exprs)) .Stmts,
       .Stmts)
    Return(Name("result"))

  rule mutatedParseMusicCharBody =>
    If(Compare(Name("char"), CmpOp("==", Str("o"))),
       Assign(Name("current"), Int(5)) .Stmts,
       If(Compare(Name("char"), CmpOp("==", Str("."))),
          Assign(Name("current"), Int(1)) .Stmts,
          If(Compare(Name("char"), CmpOp("==", Str("|"))),
             If(Compare(Name("current"), CmpOp("==", Int(4))),
                Assign(Name("current"), Int(2)) .Stmts,
                .Stmts)
             Expr(Call(Attribute(Name("result"), "append"), Name("current") , .Exprs))
             Assign(Name("current"), Int(0)),
             If(Compare(Name("current"), CmpOp("==", Int(4))),
                Expr(Call(Attribute(Name("result"), "append"), Name("current") , .Exprs)) .Stmts,
                .Stmts)
             Assign(Name("current"), Int(0)))))

  rule nextCurrent(C:Int, _:Int) => 4
    requires C ==Int 111
  rule nextCurrent(C:Int, _:Int) => 1
    requires C ==Int 46
  rule nextCurrent(C:Int, _:Int) => 0
    requires C =/=Int 111 andBool C =/=Int 46

  rule nextResult(ACC:ValSeq, C:Int, CUR:Int)
    => valSeqConcat(ACC, vCons(2, .ValSeq))
    requires C ==Int 124 andBool CUR ==Int 4
  rule nextResult(ACC:ValSeq, C:Int, CUR:Int)
    => valSeqConcat(ACC, vCons(CUR, .ValSeq))
    requires C ==Int 124 andBool CUR =/=Int 4
  rule nextResult(ACC:ValSeq, C:Int, CUR:Int)
    => valSeqConcat(ACC, vCons(4, .ValSeq))
    requires C =/=Int 111 andBool C =/=Int 46 andBool C =/=Int 124
     andBool CUR ==Int 4
  rule nextResult(ACC:ValSeq, C:Int, CUR:Int) => ACC
    requires (C ==Int 111 orBool C ==Int 46)
      orBool (C =/=Int 124 andBool CUR =/=Int 4)

  rule scanCurrent(.IntSeq, CUR:Int) => CUR
  rule scanCurrent(iCons(C:Int, REST:IntSeq), CUR:Int)
    => scanCurrent(REST, nextCurrent(C, CUR))

  rule scanResult(.IntSeq, _:Int, ACC:ValSeq) => ACC
  rule scanResult(iCons(C:Int, REST:IntSeq), CUR:Int, ACC:ValSeq)
    => scanResult(REST, nextCurrent(C, CUR), nextResult(ACC, C, CUR))

  rule musicResult(CS:IntSeq)
    => valSeqConcat(scanResult(CS, 0, .ValSeq), vCons(4, .ValSeq))
    requires scanCurrent(CS, 0) ==Int 4
  rule musicResult(CS:IntSeq) => scanResult(CS, 0, .ValSeq)
    requires scanCurrent(CS, 0) =/=Int 4
endmodule
