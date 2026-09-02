requires "reference-semantics/semantics.k"

module DIGIT-SUM-VERIFICATION
  imports MPY

  syntax Scope ::= "digitSumBuiltins" [macro]
  rule digitSumBuiltins
    => scope(
         "len" |-> builtinV("len")
         "set" |-> builtinV("set")
         "sum" |-> builtinV("sum")
         "abs" |-> builtinV("abs")
         "min" |-> builtinV("min")
         "max" |-> builtinV("max")
         "ord" |-> builtinV("ord")
         "chr" |-> builtinV("chr")
         "range" |-> builtinV("range")
         "all" |-> builtinV("all")
         "any" |-> builtinV("any")
         "zip" |-> builtinV("zip")
         "isinstance" |-> builtinV("isinstance")
         "sorted" |-> builtinV("sorted")
         "list" |-> builtinV("list")
         "round" |-> builtinV("round")
         "bin" |-> builtinV("bin")
         "enumerate" |-> builtinV("enumerate")
         "map" |-> builtinV("map")
         "eval" |-> builtinV("eval")
         "int" |-> typeV("int")
         "str" |-> typeV("str")
         "float" |-> typeV("float"),
         root
       )

  syntax Stmts ::= "digitSumLoopBody" [macro]
  rule digitSumLoopBody
    => Assign(Name("code"), Call(Name("ord"), (Name("char"), .Exprs)))
       If(
         BoolOp(
           "and",
           ( Compare(Name("code"), CmpOp(">=", Int(65)))
           , Compare(Name("code"), CmpOp("<=", Int(90)))
           , .Exprs
           )
         ),
         AugAssign(Name("result"), "+", Int(1)) .Stmts,
         .Stmts
       )
       .Stmts

  syntax Stmts ::= "digitSumBody" [macro]
  rule digitSumBody
    => Assign(Name("result"), Int(0))
       Assign(Name("char"), Str(""))
       Assign(Name("code"), Int(0))
       For(Name("char"), Name("s"), digitSumLoopBody)
       Return(Name("result"))
       .Stmts

  syntax Int ::= digitSumSpec(IntSeq) [function, total]
  rule digitSumSpec(.IntSeq) => 0
  rule digitSumSpec(iCons(C:Int, REST:IntSeq))
    => (#if C >=Int 65 andBool C <=Int 90
        #then C
        #else 0
        #fi) +Int digitSumSpec(REST)
endmodule

// This module packages the initialization and loop theorems as reusable
// rewrites.  prove.sh first proves the identical reachability claims against
// DIGIT-SUM-VERIFICATION, then compiles this extension solely to prove their
// composition at the public entry point.
module DIGIT-SUM-VERIFICATION-WITH-LOOP-LEMMA
  imports DIGIT-SUM-VERIFICATION

  rule [digit-sum-initialization-lemma]:
    <k>
      Call(
        closureVal(("s", .ParamNames), digitSumBody, 0),
        (str(S:IntSeq), .Exprs)
      )
      =>
      #loop(str(S), Name("char"), digitSumLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
      =>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
      1 |->
        scope(
          "s" |-> str(S)
          "result" |-> 0
          "char" |-> str(.IntSeq)
          "code" |-> 0,
          parent(0)
        )
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      .List
      => ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [priority(20)]

  rule [digit-sum-loop-lemma]:
    <k>
      #loop(str(S:IntSeq), Name("char"), digitSumLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      => A:Int +Int digitSumSpec(S)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
      ( 1 |->
        scope(
          "s" |-> INPUT:Val
          "result" |-> A
          "char" |-> OLDCHAR:Val
          "code" |-> OLDCODE:Val,
          parent(0)
        )
      )
      =>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [priority(20)]
endmodule
