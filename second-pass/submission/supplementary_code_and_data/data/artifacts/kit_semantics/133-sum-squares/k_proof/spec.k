requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-inv]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("number"),
        Assign(
          Name("rounded"),
          Call(Attribute(Name("math"), "ceil"), Name("number")))
        AugAssign(
          Name("total"),
          "+",
          BinOp("*", Name("rounded"), Name("rounded"))))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ("lst" |-> INPUT:Val
         "number" |-> OLDNUMBER:Val
         "rounded" |-> OLDROUNDED:Int
         "total" |-> ACC:Int)
        =>
        ("lst" |-> INPUT
         "number" |-> ?NUMBER:Val
         "rounded" |-> ?ROUNDED:Int
         "total" |-> (ACC +Int sumCeilSquares(VS))),
        parent(0))
      ...
    </scopes>

  claim [sum-squares]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("sum_squares"), list(VS:ValSeq))
      => sumCeilSquares(VS)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope)
      =>
      (0 |-> scope(?GLOBALS:Map, parent(-1))
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
