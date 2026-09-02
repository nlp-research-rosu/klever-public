requires "verification.k"

module AUDITOR-GROUND-WITNESS
  imports VERIFICATION

  claim [loop-satisfiable]:
    <k>
      #loop(
        list(
          vCons(
            str(strToCodes("abc")),
            vCons(
              str(strToCodes("bcd")),
              .ValSeq))),
        Name("string"),
        filterLoopBody)
      ~> (Return(Name("result")) .Stmts):Stmts
      ~> #endcall
      => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (.Map
       1 |-> scope(
              "strings" |->
                list(
                  vCons(
                    str(strToCodes("abc")),
                    vCons(
                      str(strToCodes("bcd")),
                      .ValSeq)))
              "prefix" |-> str(strToCodes("a"))
              "result" |-> ref(0)
              "string" |-> str(.IntSeq),
              parent(0)))
      => .Map
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      0 |-> list(
             vCons(
               str(strToCodes("seed")),
               .ValSeq)
             =>
             vCons(
               str(strToCodes("seed")),
               vCons(
                 str(strToCodes("abc")),
                 .ValSeq)))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [program-satisfiable]:
    <k>
      #loadAll(filterByPrefixProgram)
      ~> Call(
           Name("filter_by_prefix"),
           list(
             vCons(
               str(strToCodes("abc")),
               vCons(
                 str(strToCodes("bcd")),
                 vCons(
                   str(.IntSeq),
                   vCons(
                     str(strToCodes("array")),
                     .ValSeq))))),
           str(strToCodes("a")))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             .Map
             => "filter_by_prefix" |->
                  closureVal(
                    ("strings", "prefix"),
                    filterFunctionBody,
                    0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           vCons(
             str(strToCodes("abc")),
             vCons(
               str(strToCodes("array")),
               .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
