requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [sum-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("number"),
        Assign(Name("total"),
               BinOp("+", Name("total"), Name("number"))) .Stmts)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "mean_absolute_deviation"
              |-> closureVal(("numbers", .ParamNames), madBody, 0),
              parent(-1))
       1 |-> scope(
              "count"   |-> COUNT:Int
              "number"  |-> (_OLD:Val => ?FINAL:Val)
              "numbers" |-> list(ALL:ValSeq)
              "total"   |-> (ACC:Float => sumFloatVS(VS, ACC)),
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatVS(VS)

  claim [deviation-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("number"),
        Assign(
          Name("deviation"),
          BinOp(
            "+",
            Name("deviation"),
            Call(Name("abs"),
                 BinOp("-", Name("number"), Name("mean"))))) .Stmts)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "mean_absolute_deviation"
              |-> closureVal(("numbers", .ParamNames), madBody, 0),
              parent(-1))
       1 |-> scope(
              "count"     |-> COUNT:Int
              "deviation" |-> (ACC:Float
                                => deviationFloatVS(VS, MEAN, ACC))
              "mean"      |-> MEAN:Float
              "number"    |-> (_OLD:Val => ?FINAL:Val)
              "numbers"   |-> list(ALL:ValSeq)
              "total"     |-> TOTAL:Float,
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatVS(VS)

  claim [mean-absolute-deviation]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef(
            "mean_absolute_deviation",
            Params("numbers"),
            madBody)))
      ~> Call(Name("mean_absolute_deviation"), (list(VS:ValSeq), .Exprs))
      => madResult(VS)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              .Map
              => "mean_absolute_deviation"
                 |-> closureVal(("numbers", .ParamNames), madBody, 0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloatVS(VS)
endmodule
