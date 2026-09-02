requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The constructor term generated in solution.mpy, factored only so that the
  // loop body can also be named in the inductive claim.
  syntax Stmts ::= "arrangeBody" [function]
  rule arrangeBody
    => If(Compare(Name("index"), CmpOp(">", Int(0))),
         If(Compare(Name("current"), CmpOp("<", Name("previous"))),
            Assign(Name("result"), Name("index")),
            .Stmts),
         .Stmts)
       Assign(Name("previous"), Name("current"))
       Assign(Name("index"), BinOp("+", Name("index"), Int(1)))

  syntax Module ::= "solutionProgram" [function]
  rule solutionProgram
    => Module(
         FuncDef("can_arrange", Params("arr"),
           Assign(Name("result"), UnaryOp("-", Int(1)))
           Assign(Name("index"), Int(0))
           Assign(Name("previous"), Int(0))
           For(Name("current"), Name("arr"), arrangeBody)
           Return(Name("result"))))

  // Domain predicate: every element in the HumanEval array is an integer.
  syntax Bool ::= ints(ValSeq) [function, total]
  rule ints(.ValSeq) => true
  rule ints(vCons(V:Val, REST:ValSeq))
    => isInt(V) andBool ints(REST)

  // A proof-only sort refinement. The iterator protocol yields a generic Val
  // even when `ints` proves that value is an Int. `intValue` gives SMT an
  // Int-sorted view and agrees definitionally with every concrete Int.
  syntax Int ::= intValue(Val) [function, total]
  rule intValue(I:Int) => I

  rule applyCmp("<", L:Val, R:Val)
    => intValue(L) <Int intValue(R)
    requires isInt(L) andBool isInt(R)

  // Mathematical result of scanning the unprocessed suffix.  INDEX is the
  // next absolute index, PREVIOUS is the preceding item (ignored at index 0),
  // and RESULT is the latest violating index seen so far.
  syntax Int ::= arrangeResult(ValSeq) [function]
               | arrangeScan(ValSeq, Int, Val, Int) [function]
  rule arrangeResult(VS:ValSeq) => arrangeScan(VS, 0, 0, -1)
  rule arrangeScan(.ValSeq, _:Int, _:Val, RESULT:Int) => RESULT
  rule arrangeScan(vCons(CURRENT:Val, REST:ValSeq),
                   INDEX:Int, PREVIOUS:Val, RESULT:Int)
    => arrangeScan(
         REST,
         INDEX +Int 1,
         CURRENT,
         #if INDEX >Int 0
               andBool intValue(CURRENT) <Int intValue(PREVIOUS)
         #then INDEX
         #else RESULT
         #fi)
    requires isInt(CURRENT)
     andBool (INDEX ==Int 0 orBool isInt(PREVIOUS))
endmodule
