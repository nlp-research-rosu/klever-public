requires "verification.k"

module HISTOGRAM-SPEC-LABELED
  imports VERIFICATION

  claim [claim-01]:
    <k>
      #loadAll(histogramCheck(
        Str(""),
        DictExpr(.Entries)))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [claim-02]:
    <k>
      #loadAll(histogramCheck(
        Str("a b c"),
        DictExpr(
          Entry(Str("a"), Int(1)),
          Entry(Str("b"), Int(1)),
          Entry(Str("c"), Int(1)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [claim-03]:
    <k>
      #loadAll(histogramCheck(
        Str("a b b a"),
        DictExpr(
          Entry(Str("a"), Int(2)),
          Entry(Str("b"), Int(2)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [claim-04]:
    <k>
      #loadAll(histogramCheck(
        Str("a b c a b"),
        DictExpr(
          Entry(Str("a"), Int(2)),
          Entry(Str("b"), Int(2)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [claim-05]:
    <k>
      #loadAll(histogramCheck(
        Str("b b b b a"),
        DictExpr(Entry(Str("b"), Int(4)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // For every token value A, a one-token input returns exactly A |-> 1.
  claim [claim-06]:
    <k>
      #loadAll(histogramCheck(
        str(tokenText(vCons(str(A:IntSeq), .ValSeq))),
        DictExpr(Entry(str(A), Int(1)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Repeated symbolic token: the counter is incremented, not duplicated.
  claim [claim-07]:
    <k>
      #loadAll(histogramCheck(
        str(tokenText(
          vCons(str(A:IntSeq),
          vCons(str(A), .ValSeq)))),
        DictExpr(Entry(str(A), Int(2)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Two distinct symbolic tokens tie and retain their input order.
  claim [claim-08]:
    <k>
      #loadAll(histogramCheck(
        str(tokenText(
          vCons(str(A:IntSeq),
          vCons(str(B:IntSeq), .ValSeq)))),
        DictExpr(
          Entry(str(A), Int(1)),
          Entry(str(B), Int(1)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (A ==K B)

  // Three-token equality partitions exercise each maximum/tie shape.
  claim [claim-09]:
    <k>
      #loadAll(histogramCheck(
        str(tokenText(
          vCons(str(A:IntSeq),
          vCons(str(A),
          vCons(str(A), .ValSeq))))),
        DictExpr(Entry(str(A), Int(3)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [claim-10]:
    <k>
      #loadAll(histogramCheck(
        str(tokenText(
          vCons(str(A:IntSeq),
          vCons(str(A),
          vCons(str(B:IntSeq), .ValSeq))))),
        DictExpr(Entry(str(A), Int(2)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (A ==K B)

  claim [claim-11]:
    <k>
      #loadAll(histogramCheck(
        str(tokenText(
          vCons(str(A:IntSeq),
          vCons(str(B:IntSeq),
          vCons(str(A), .ValSeq))))),
        DictExpr(Entry(str(A), Int(2)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (A ==K B)

  claim [claim-12]:
    <k>
      #loadAll(histogramCheck(
        str(tokenText(
          vCons(str(A:IntSeq),
          vCons(str(B:IntSeq),
          vCons(str(B), .ValSeq))))),
        DictExpr(Entry(str(B), Int(2)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (A ==K B)

  claim [claim-13]:
    <k>
      #loadAll(histogramCheck(
        str(tokenText(
          vCons(str(A:IntSeq),
          vCons(str(B:IntSeq),
          vCons(str(C:IntSeq), .ValSeq))))),
        DictExpr(
          Entry(str(A), Int(1)),
          Entry(str(B), Int(1)),
          Entry(str(C), Int(1)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (A ==K B)
     andBool notBool (A ==K C)
     andBool notBool (B ==K C)
endmodule
