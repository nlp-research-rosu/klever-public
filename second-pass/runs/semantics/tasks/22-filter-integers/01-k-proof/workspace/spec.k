requires "verification.k"

module FILTER-SPEC
  imports FILTER-VERIFICATION

  claim [empty]:
    <k> #loadAll(FILTER-PROGRAM)
         ~> Call(Name("filter_integers"), list(.ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0  |-> scope("filter_integers" |-> FILTER-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Symbolic form of the first prompt example: arbitrary string, float, and
  // integer values in the same positions.
  claim [prompt-example-one]:
    <k> #loadAll(FILTER-PROGRAM)
         ~> Call(
              Name("filter_integers"),
              list(vCons(str(S:IntSeq),
                   vCons(F:Float,
                   vCons(I:Int, .ValSeq)))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0  |-> scope("filter_integers" |-> FILTER-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(I, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Symbolic form of the second prompt example.  The non-integers include a
  // string, dictionary, and list semantic value.
  claim [prompt-example-two]:
    <k> #loadAll(FILTER-PROGRAM)
         ~> Call(
              Name("filter_integers"),
              list(vCons(I1:Int,
                   vCons(I2:Int,
                   vCons(I3:Int,
                   vCons(str(S:IntSeq),
                   vCons(dictV(.ValSeq, .ValSeq),
                   vCons(list(.ValSeq), .ValSeq))))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0  |-> scope("filter_integers" |-> FILTER-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(vCons(I1, vCons(I2, vCons(I3, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Order preservation with interleaved symbolic integers and other supported
  // scalar values.  Bool is intentionally non-Int in the supplied semantics.
  claim [order-and-scalars]:
    <k> #loadAll(FILTER-PROGRAM)
         ~> Call(
              Name("filter_integers"),
              list(vCons(B:Bool,
                   vCons(A:Int,
                   vCons(noneV,
                   vCons(str(S:IntSeq),
                   vCons(C:Int, .ValSeq)))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0  |-> scope("filter_integers" |-> FILTER-CLOSURE, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(vCons(A, vCons(C, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
