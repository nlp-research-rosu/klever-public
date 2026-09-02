requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-inv]:
    <k>
      #loop(
        str(CS:IntSeq),
        Name("char"),
        AugAssign(
          Name("count"),
          "+",
          Compare(Name("char"), CmpOp("in", Str("aeiouAEIOU"))))
        Assign(Name("last"), Name("char"))
        .Stmts)
      ~> AugAssign(
           Name("count"),
           "+",
           Compare(Name("last"), CmpOp("==", Str("y"))))
         AugAssign(
           Name("count"),
           "+",
           Compare(Name("last"), CmpOp("==", Str("Y"))))
         Return(Name("count"))
         .Stmts
      ~> #endcall
      =>
      (COUNT:Int +Int vowelsTail(CS, LAST:IntSeq)) ~> CONT:K
    </k>
    <env> 1 => CALLER:Int </env>
    <scopes>
      (0 |-> scope(GLOBAL:Map, parent(-1))
       1 |-> scope(
         "s" |-> str(ORIGINAL:IntSeq)
         "count" |-> COUNT
         "last" |-> str(LAST)
         "char" |-> CHAR:Val,
         parent(0))
       -1 |-> BUILTINS:Scope)
      =>
      (0 |-> scope(GLOBAL, parent(-1))
       -1 |-> BUILTINS)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack>
      ListItem(frame(CONT, CALLER, 1)) CALLSTACK:List
      =>
      CALLSTACK
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [vowels-count]:
    <k>
      #loadAll(Module(
        FuncDef(
          "vowels_count",
          Params("s"),
          Assign(Name("count"), Int(0))
          Assign(Name("last"), Str(""))
          Assign(Name("char"), Str(""))
          For(
            Name("char"),
            Name("s"),
            AugAssign(
              Name("count"),
              "+",
              Compare(Name("char"), CmpOp("in", Str("aeiouAEIOU"))))
            Assign(Name("last"), Name("char"))
            .Stmts)
          AugAssign(
            Name("count"),
            "+",
            Compare(Name("last"), CmpOp("==", Str("y"))))
          AugAssign(
            Name("count"),
            "+",
            Compare(Name("last"), CmpOp("==", Str("Y"))))
          Return(Name("count"))
          .Stmts)
        .Stmts))
      ~> Call(Name("vowels_count"), (str(INPUT:IntSeq), .Exprs))
      =>
      vowelsTail(INPUT, .IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
         "vowels_count" |-> closureVal(
           ("s", .ParamNames),
           Assign(Name("count"), Int(0))
           Assign(Name("last"), Str(""))
           Assign(Name("char"), Str(""))
           For(
             Name("char"),
             Name("s"),
             AugAssign(
               Name("count"),
               "+",
               Compare(Name("char"), CmpOp("in", Str("aeiouAEIOU"))))
             Assign(Name("last"), Name("char"))
             .Stmts)
           AugAssign(
             Name("count"),
             "+",
             Compare(Name("last"), CmpOp("==", Str("y"))))
           AugAssign(
             Name("count"),
             "+",
             Compare(Name("last"), CmpOp("==", Str("Y"))))
           Return(Name("count"))
           .Stmts,
           0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
