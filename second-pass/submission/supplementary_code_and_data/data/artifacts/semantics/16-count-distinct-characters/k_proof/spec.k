requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loading the translated definition creates precisely the closure used below.
  claim
    <k> #loadCountDistinct => .K </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(
        ("count_distinct_characters"
          |-> closureVal(
            ("string", .ParamNames),
            Return(
              Call(
                Name("len"),
                Call(
                  Name("set"),
                  Call(Attribute(Name("string"), "lower"), .Exprs))))
            .Stmts,
            0)),
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // For every semantic string, the implementation returns the number of
  // distinct codes after applying the supplied Python-lowercase model.
  claim
    <k>
      #callCountDistinct(CS:IntSeq)
      =>
      isLen(dedupCodes(mapLower(CS)))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
