requires "verification-real-list.k"

module FILTER-BY-PREFIX-REAL-LIST-SPEC
  imports VERIFICATION-REAL-LIST

  // Bridge-free invariant over the fixed semantics' actual list(ValSeq).
  claim
    <k>
      #loop(
        list(strValues(REST:StrList)),
        Name("string"),
        If(
          Call(Attribute(Name("string"), "startswith"), Name("prefix")),
          Expr(Call(Attribute(Name("result"), "append"), Name("string"))),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        "prefix" |-> str(PREFIX:IntSeq)
        "result" |-> ref(H:Int)
        "string" |-> CURRENT:Val
        "strings" |-> list(strValues(ORIGINAL:StrList)),
        parent(0))
      =>
      SC
      L |-> scope(
        "prefix" |-> str(PREFIX)
        "result" |-> ref(H)
        "string" |-> ?FINALCURRENT:Val
        "strings" |-> list(strValues(ORIGINAL)),
        parent(0))
    </scopes>
    <heap>
      H |-> list(
        ACC:ValSeq
        => valSeqConcat(ACC, prefixFilter(PREFIX, REST)))
    </heap>

  // End-to-end theorem over fixed-semantics list values, without stringList.
  claim
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          filterByPrefixDef))
      ~> Call(
           Name("filter_by_prefix"),
           list(strValues(INPUT:StrList)),
           str(PREFIX:IntSeq))
      ~> #checkFilter(prefixFilter(PREFIX, INPUT))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => ?FINALSC:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(prefixFilter(PREFIX, INPUT))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
