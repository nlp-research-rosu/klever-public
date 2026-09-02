requires "/tmp/audit-work/source/verification.k"

module GROUND-SPEC
  imports VERIFICATION

  claim [empty]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "odd_count",
            Params(("lst", .ParamNames)),
            oddBody)))
      ~> Call(
           Name("odd_count"),
           (list(INPUT:ValSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "odd_count" |-> closureVal(
                 ("lst", .ParamNames),
                 oddBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires INPUT ==K .ValSeq

  claim [prompt-one]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "odd_count",
            Params(("lst", .ParamNames)),
            oddBody)))
      ~> Call(
           Name("odd_count"),
           (list(INPUT:ValSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "odd_count" |-> closureVal(
                 ("lst", .ParamNames),
                 oddBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             vCons(
               str(strToCodes(
                 "the number of odd elements 4n the str4ng 4 of the 4nput.")),
               .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires INPUT
             ==K vCons(str(strToCodes("1234567")), .ValSeq)

  claim [prompt-two]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "odd_count",
            Params(("lst", .ParamNames)),
            oddBody)))
      ~> Call(
           Name("odd_count"),
           (list(INPUT:ValSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "odd_count" |-> closureVal(
                 ("lst", .ParamNames),
                 oddBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             vCons(
               str(strToCodes(
                 "the number of odd elements 1n the str1ng 1 of the 1nput.")),
               vCons(
                 str(strToCodes(
                   "the number of odd elements 8n the str8ng 8 of the 8nput.")),
                 .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires INPUT
             ==K vCons(
                   str(strToCodes("3")),
                   vCons(str(strToCodes("11111111")), .ValSeq))

  claim [ten-odd]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "odd_count",
            Params(("lst", .ParamNames)),
            oddBody)))
      ~> Call(
           Name("odd_count"),
           (list(INPUT:ValSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "odd_count" |-> closureVal(
                 ("lst", .ParamNames),
                 oddBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             vCons(
               str(strToCodes(
                 "the number of odd elements 10n the str10ng 10 of the 10nput.")),
               .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires INPUT
             ==K vCons(str(strToCodes("1111111111")), .ValSeq)
endmodule
