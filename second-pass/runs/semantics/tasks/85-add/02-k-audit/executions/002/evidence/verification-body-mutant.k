requires "/tmp/audit-work/85-add/reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax ValSeq ::= intVals(IntSeq)
  rule <k> #iterNext(list(intVals(.IntSeq))) => #iterDone ... </k>
       [priority(40)]
  rule <k> #iterNext(list(intVals(iCons(I:Int, REST:IntSeq))))
        => #iterYield(I, list(intVals(REST))) ... </k>
       [priority(40)]

  syntax Int ::= addAccSpec(IntSeq, Bool, Int) [function]
  rule addAccSpec(.IntSeq, _:Bool, ACC:Int) => ACC
  rule addAccSpec(iCons(_:Int, REST:IntSeq), false, ACC:Int)
    => addAccSpec(REST, true, ACC)
  rule addAccSpec(iCons(I:Int, REST:IntSeq), true, ACC:Int)
    => addAccSpec(REST, false, ACC +Int I)
    requires pyMod(I, 2) ==Int 0
  rule addAccSpec(iCons(I:Int, REST:IntSeq), true, ACC:Int)
    => addAccSpec(REST, false, ACC)
    requires pyMod(I, 2) =/=Int 0

  syntax Stmts ::= "addLoopBody" [macro]
  rule addLoopBody
    => If(Name("odd_index"),
         If(Compare(BinOp("%", Name("value"), Int(2)),
                    CmpOp("==", Int(0))),
            AugAssign(Name("total"), "+", Name("value")),
            .Stmts),
         .Stmts)
       Assign(Name("odd_index"), UnaryOp("not", Name("odd_index")))

  syntax Stmts ::= "mutatedFunctionBody" [macro]
  rule mutatedFunctionBody
    => Expr(Str("Add the even elements that occur at odd zero-based indices."))
       Assign(Name("total"), Int(0))
       Assign(Name("odd_index"), Bool(false))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("lst"),
         Assign(Name("total"), Int(1)))
       Return(Name("total"))

  syntax Module ::= "mutatedSolutionModule" [macro]
  rule mutatedSolutionModule
    => Module(FuncDef("add", Params("lst"), mutatedFunctionBody))

  // Candidate bridge retained unchanged: it matches only the original body,
  // so it cannot summarize the mutated For term above.
  rule <k>
         #loop(list(intVals(INPUT:IntSeq)), Name("value"), addLoopBody)
         ~> (Return(Name("total")) .Stmts):Stmts
         ~> #endcall
       =>
         Return(addAccSpec(INPUT, false, 0))
         ~> #endcall
       ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("lst" |-> list(intVals(INPUT)))
           ("total" |-> 0)
           ("odd_index" |-> false)
           ("value" |-> 0),
           _:Parent)
         ...
       </scopes>
       [priority(30)]
endmodule
