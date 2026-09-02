requires "reference-semantics/semantics.k"

module BELOW-ZERO-COMMON
  imports MPY

  // These aliases are the exact constructor terms emitted in solution.mpy.
  syntax Stmts ::= "belowZeroLoopBody" [macro]
  rule belowZeroLoopBody
    => AugAssign(Name("balance"), "+", Name("operation"))
       If(Compare(Name("balance"), CmpOp("<", Int(0))),
          Return(Bool(true)) .Stmts,
          .Stmts)

  syntax Stmts ::= "belowZeroFunctionBody" [macro]
  rule belowZeroFunctionBody
    => Assign(Name("balance"), Int(0))
       Assign(Name("operation"), Int(0))
       For(Name("operation"), Name("operations"), belowZeroLoopBody)
       Return(Bool(false))

  syntax Module ::= "solutionProgram" [macro]
  rule solutionProgram
    => Module(
         ImportFrom("typing", "List")
         FuncDef("below_zero", Params("operations"), belowZeroFunctionBody))

  // An inductive, integer-only symbolic presentation of every finite
  // List[int].  Its iterator equations are exactly the .ValSeq/vCons cases
  // from MPY-LIST, but preserve an Int-sorted head during symbolic induction.
  syntax IntVals ::= ".IntVals" | intCons(Int, IntVals)
  syntax ValSeq ::= asValSeq(IntVals)
  rule <k> #iterNext(list(asValSeq(.IntVals))) => #iterDone ... </k>
  rule <k> #iterNext(list(asValSeq(intCons(I:Int, IS:IntVals))))
        => #iterYield(I, list(asValSeq(IS))) ... </k>

  // Mathematical contract: some running balance, starting at B, is negative.
  syntax Bool ::= prefixBelow(Int, IntVals) [function, total]
  rule prefixBelow(_:Int, .IntVals) => false
  rule prefixBelow(B:Int, intCons(I:Int, IS:IntVals))
    => #if B +Int I <Int 0
       #then true
       #else prefixBelow(B +Int I, IS)
       #fi
endmodule

module MPY-VERIFICATION
  imports BELOW-ZERO-COMMON
endmodule

module MPY-VERIFICATION-LEMMA
  imports BELOW-ZERO-COMMON

  // This is admitted only in the definition used for the top-level claim.
  // AUX-SPEC proves this exact reachability step first against MPY itself.
  rule
    <k> #loop(list(asValSeq(IS:IntVals)), Name("operation"), belowZeroLoopBody)
         ~> (Return(Bool(false)) .Stmts) ~> #endcall
      => prefixBelow(B, IS)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(MODULE:Map, parent(-1))
      -1 |-> BUILTINS:Scope
      1 |-> scope(
        "operations" |-> list(asValSeq(INPUT:IntVals))
        "operation"  |-> OLD:Val
        "balance"    |-> B:Int,
        parent(0))
      =>
      0 |-> scope(MODULE, parent(-1))
      -1 |-> BUILTINS
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [priority(40)]
endmodule
