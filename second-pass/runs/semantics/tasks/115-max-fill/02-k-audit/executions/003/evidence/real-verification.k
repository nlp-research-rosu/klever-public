requires "verification.k"

module REAL-VERIFICATION
  imports MAX-FILL-DATA

  syntax Val ::= realFinalRow(GridRows, Val) [function, total]
  syntax Int ::= realFinalWater(GridRows, Int) [function, total]

  rule realFinalRow(.GridRows, V:Val) => V
  rule realFinalRow(gCons(IS:IntSeq, GS:GridRows), _V:Val)
    => realFinalRow(GS, list(rowVals(IS)))

  rule realFinalWater(.GridRows, W:Int) => W
  rule realFinalWater(gCons(IS:IntSeq, GS:GridRows), _W:Int)
    => realFinalWater(GS, rowSum(IS))

  syntax KItem ::= #runMaxFillReal(GridRows, Int)
  rule <k> #runMaxFillReal(GS:GridRows, C:Int)
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
           ~> Call(Name("max_fill"), list(gridVals(GS)), C)
           ...
       </k>
endmodule
