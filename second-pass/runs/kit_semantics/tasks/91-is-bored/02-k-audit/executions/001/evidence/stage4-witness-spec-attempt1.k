requires "verification.k"

module STAGE4-WITNESS-SPEC
  imports VERIFICATION

  claim [empty-entry-witness]:
    <k>
      Call(Name("is_bored"), (str(.IntSeq), .Exprs))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "is_bored" |-> closureVal(
          ("S", .ParamNames),
          BORED-FUNCTION-BODY,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [i-work-entry-witness]:
    <k>
      Call(
        Name("is_bored"),
        ( str(
            iCons(73,
              iCons(32,
                iCons(119,
                  iCons(111,
                    iCons(114,
                      iCons(107, .IntSeq)))))))
          ),
          .Exprs )
      )
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "is_bored" |-> closureVal(
          ("S", .ParamNames),
          BORED-FUNCTION-BODY,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
