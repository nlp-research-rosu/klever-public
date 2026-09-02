requires "reference-semantics/semantics.k"

module MAX-FILL-DATA
  imports MPY

  // A symbolic grid whose rows contain integers.  This representation includes
  // every grid allowed by the prompt (whose integers are restricted to 0/1).
  syntax GridRows ::= ".GridRows"
                    | gCons(IntSeq, GridRows)

  syntax ValSeq ::= rowVals(IntSeq) [function, total]
                  | gridVals(GridRows) [function, total]

  rule rowVals(.IntSeq)                 => .ValSeq
  rule rowVals(iCons(I:Int, IS:IntSeq)) => vCons(I, rowVals(IS))

  rule gridVals(.GridRows) => .ValSeq
  rule gridVals(gCons(IS:IntSeq, GS:GridRows))
    => vCons(list(rowVals(IS)), gridVals(GS))

  // Mathematical contract: sum a row, take ceil(sum / capacity), and add
  // those bucket counts for all rows.  ceilDiv is written with the same
  // integer floor-division primitive used by MPY-INT.
  syntax Int ::= rowSum(IntSeq) [function, total]
               | rowTotal(Int, IntSeq) [function, total]
               | ceilDiv(Int, Int) [function, total]
               | fillTotal(Int, GridRows, Int) [function, total]
               | maxFillSpec(GridRows, Int) [function, total]

  rule rowSum(IS:IntSeq) => rowTotal(0, IS)
  rule rowTotal(A:Int, .IntSeq) => A
  rule rowTotal(A:Int, iCons(I:Int, IS:IntSeq))
    => rowTotal(A +Int I, IS)

  rule ceilDiv(N:Int, C:Int)
    => ((N +Int C -Int 1) -Int pyMod(N +Int C -Int 1, C)) /Int C

  rule fillTotal(A:Int, .GridRows, _C:Int) => A
  rule fillTotal(A:Int, gCons(IS:IntSeq, GS:GridRows), C:Int)
    => fillTotal(A +Int ceilDiv(rowSum(IS), C), GS, C)
  rule maxFillSpec(GS:GridRows, C:Int) => fillTotal(0, GS, C)

  // Exact translated loop body from solution.mpy.
  syntax Stmts ::= "MAX_FILL_LOOP_BODY" [macro]
  rule MAX_FILL_LOOP_BODY
    => Assign(Name("water"), Call(Name("sum"), Name("row")))
       AugAssign(
         Name("result"),
         "+",
         BinOp(
           "//",
           BinOp(
             "-",
             BinOp("+", Name("water"), Name("capacity")),
             Int(1)),
           Name("capacity")))
       .Stmts

endmodule

// One-step symbolic bridges for the typed constructor representation above.
// Each bridge is separately proved against MAX-FILL-DATA (which imports only
// MPY) before this module is used by the unbounded proof.
module MAX-FILL-BRIDGES
  imports MAX-FILL-DATA

  // Opaque, typed symbolic sequences.  Their iterator dispatch below is the
  // executable abstraction justified by the concrete rowVals/gridVals bridge
  // claims in MAX-FILL-BRIDGE-SPEC.
  syntax ValSeq ::= symRow(IntSeq)
                  | symGrid(GridRows)

  syntax KItem ::= #typedSum(IntSeq, Int)
                 | #typedLoop(GridRows, Expr, Stmts)

  // Dispatch abstract constructor sequences before the generic MPY iterator
  // rules forget their element/row sorts.  The two constructor cases below
  // are exactly the four transitions proved in MAX-FILL-BRIDGE-SPEC.
  rule <k> #sumAcc(list(symRow(IS:IntSeq)), A:Int)
        => #typedSum(IS, A)
        ...
       </k>
       [priority(40)]

  rule <k> #typedSum(.IntSeq, A:Int)
        => #iterNext(list(.ValSeq)) ~> #sumCont(A)
        ...
       </k>

  rule <k> #typedSum(iCons(I:Int, IS:IntSeq), A:Int)
        => #iterNext(list(vCons(I +Int 1, symRow(IS)))) ~> #sumCont(A)
        ...
       </k>

  rule <k> #loop(
             list(symGrid(GS:GridRows)),
             T:Expr,
             B:Stmts)
        => #typedLoop(GS, T, B)
        ...
       </k>
       [priority(40)]

  rule <k> #typedLoop(.GridRows, T:Expr, B:Stmts)
        => #iterNext(list(.ValSeq)) ~> #loopStep(T, B)
        ...
       </k>

  rule <k> #typedLoop(
             gCons(IS:IntSeq, GS:GridRows),
             T:Expr,
             B:Stmts)
        => #iterNext(
             list(vCons(list(symRow(IS)), symGrid(GS))))
           ~> #loopStep(T, B)
        ...
       </k>

  syntax Val ::= finalRow(GridRows, Val) [function, total]
  syntax Int ::= finalWater(GridRows, Int) [function, total]

  rule finalRow(.GridRows, V:Val) => V
  rule finalRow(gCons(IS:IntSeq, GS:GridRows), _V:Val)
    => finalRow(GS, list(symRow(IS)))

  rule finalWater(.GridRows, W:Int) => W
  rule finalWater(gCons(IS:IntSeq, GS:GridRows), _W:Int)
    => finalWater(GS, rowSum(IS))
endmodule

module MAX-FILL-VERIFICATION
  imports MAX-FILL-BRIDGES

  // A closed driver that loads and invokes the exact translated entry point.
  // Keeping the AST here makes the reachability claim execute the program
  // itself rather than a hand-written summary of it.
  syntax KItem ::= #runMaxFill(GridRows, Int)
  rule <k> #runMaxFill(GS:GridRows, C:Int)
        => #loadAll(
             Module(
               FuncDef(
                 "max_fill",
                 Params("grid", "capacity"),
                 Assign(Name("result"), Int(0))
                 Assign(Name("row"), Int(0))
                 Assign(Name("water"), Int(0))
                 For(
                   Name("row"),
                   Name("grid"),
                   MAX_FILL_LOOP_BODY)
                 Return(Name("result")))))
           ~> Call(Name("max_fill"), list(symGrid(GS)), C)
           ...
       </k>
endmodule
