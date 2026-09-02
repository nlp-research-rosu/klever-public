requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  // A declarative fold used only on claim right-hand sides.  It describes
  // the mathematical result of consuming a valid suffix from loop state
  // (CUR, DEPTH, ACC), independently of Python control-flow machinery.
  syntax ValSeq ::= scanGroups(IntSeq, IntSeq, Int, ValSeq) [function, total]
  rule scanGroups(.IntSeq, _CUR:IntSeq, _DEPTH:Int, ACC:ValSeq)
    => ACC
  rule scanGroups(iCons(32, REST:IntSeq), CUR:IntSeq,
                  DEPTH:Int, ACC:ValSeq)
    => scanGroups(REST, CUR, DEPTH, ACC)
  rule scanGroups(iCons(40, REST:IntSeq), CUR:IntSeq,
                  DEPTH:Int, ACC:ValSeq)
    => scanGroups(REST,
                  seqConcat(CUR, iCons(40, .IntSeq)),
                  DEPTH +Int 1,
                  ACC)
  rule scanGroups(iCons(C:Int, REST:IntSeq), CUR:IntSeq,
                  DEPTH:Int, ACC:ValSeq)
    => scanClose(C, REST, CUR, DEPTH, ACC)
    [owise]

  syntax ValSeq ::= scanClose(Int, IntSeq, IntSeq, Int, ValSeq)
                    [function, total]
  rule scanClose(C:Int, REST:IntSeq, CUR:IntSeq,
                 DEPTH:Int, ACC:ValSeq)
    => scanGroups(
         REST,
         .IntSeq,
         0,
         valSeqConcat(
           ACC,
           vCons(str(seqConcat(CUR, iCons(C, .IntSeq))), .ValSeq)))
    requires DEPTH -Int 1 ==Int 0
  rule scanClose(C:Int, REST:IntSeq, CUR:IntSeq,
                 DEPTH:Int, ACC:ValSeq)
    => scanGroups(REST,
                  seqConcat(CUR, iCons(C, .IntSeq)),
                  DEPTH -Int 1,
                  ACC)
    requires DEPTH -Int 1 =/=Int 0

  // balancedTail(CODES, DEPTH) is the contract domain: only spaces and
  // parentheses occur, no suffix prefix underflows DEPTH, and final depth is
  // zero. This admits spaces anywhere and adjacent top-level groups.
  syntax Bool ::= balancedTail(IntSeq, Int) [function, total]
  rule balancedTail(.IntSeq, DEPTH:Int) => DEPTH ==Int 0
  rule balancedTail(iCons(32, REST:IntSeq), DEPTH:Int)
    => balancedTail(REST, DEPTH)
  rule balancedTail(iCons(40, REST:IntSeq), DEPTH:Int)
    => balancedTail(REST, DEPTH +Int 1)
  rule balancedTail(iCons(C:Int, REST:IntSeq), DEPTH:Int)
    => C ==Int 41 andBool DEPTH >Int 0
       andBool balancedTail(REST, DEPTH -Int 1)
    requires C =/=Int 32 andBool C =/=Int 40

  syntax Bool ::= parenSpaceOnly(IntSeq) [function, total]
  rule parenSpaceOnly(.IntSeq) => true
  rule parenSpaceOnly(iCons(C:Int, REST:IntSeq))
    => (C ==Int 32 orBool C ==Int 40 orBool C ==Int 41)
       andBool parenSpaceOnly(REST)

  // The closure below is the exact FuncDef body emitted in solution.mpy.
  // Naming it keeps the claims readable; the macro adds no behavior.
  syntax Val ::= "solutionClosure" [macro]
  rule solutionClosure
    => closureVal(
         ("paren_string", .ParamNames),
         Assign(Name("groups"), ListExpr(.Exprs))
         Assign(Name("current"), Str(""))
         Assign(Name("depth"), Int(0))
         For(Name("character"), Name("paren_string"),
           If(Compare(Name("character"), CmpOp("==", Str(" "))),
             Continue .Stmts,
             .Stmts)
           AugAssign(Name("current"), "+", Name("character"))
           If(Compare(Name("character"), CmpOp("==", Str("("))),
             AugAssign(Name("depth"), "+", Int(1)) .Stmts,
             AugAssign(Name("depth"), "+", Int(1)) .Stmts)
           If(Compare(Name("depth"), CmpOp("==", Int(0))),
             Expr(Call(Attribute(Name("groups"), "append"),
                       (Name("current"), .Exprs)))
             Assign(Name("current"), Str(""))
             .Stmts,
             .Stmts)
           .Stmts)
         Return(Name("groups"))
         .Stmts,
         0)

endmodule
