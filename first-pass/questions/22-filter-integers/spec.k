// spec.k — filter_integers on the UNIFIED semantics (src/). Single index-loop filter: one loop
// invariant (i-scan appending values[i] when isinstance(values[i], int)) + entry. isinstance is
// intercepted to the opaque isIntElemV(valSeqAt(VS, I)) (verification.k), so the filter STRUCTURE folds
// via intFilter case-splitting on it; the predicate's meaning is trusted (real in krun). See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module FILTER-INTEGERS-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FILTER-INTEGERS-SPEC

requires "verification.k"

module FILTER-INTEGERS-SPEC
  imports FILTER-INTEGERS-VERIFICATION

  // ---- LOOP invariant (i-scan) — leaves result := list(intFilter(I, N, VS, R)). values/int_type
  // loop-constant; `int_type` is `int` pre-bound as a LOCAL (typeV("int")) so the isinstance type arg
  // resolves without traversing to the builtins frame (unreachable through the symbolic parent). I >= 0
  // and N == vsLen(VS) so normIdx(I, vsLen(VS)) collapses to I and the isIntElemV interception /
  // append target line up with valSeqAt(VS, I).
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(Call(Name("isinstance"), (Subscript(Name("values"), Name("i")), Name("int_type"))),
          Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Subscript(Name("values"), Name("i"))))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "filter_integers" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "values" <- list(VS:ValSeq) ] [ "result" <- ref(HN1_0:Int) ] [ "int_type" <- typeV("int") ] [ "i" <- _:Val ], parent(0))
               => scope(.Map [ "values" <- list(VS) ] [ "result" <- ref(?HN1_0B:Int) ] [ "int_type" <- typeV("int") ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(intFilter(I, N, VS, R))) ?FRESH1:Map HRST1 </heap>
    <heapLoc> HLC1:Int => ?HLC2:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool N ==Int vsLen(VS) andBool allFlat(VS)
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
     andBool notBool (HN1_0 in_keys(HRST1))
    ensures 0 <=Int ?HN1_0B andBool ?HN1_0B <Int ?HLC2 andBool HLC1 <=Int ?HLC2
     andBool keysBelow(?FRESH1, ?HLC2)
     andBool notBool (?HN1_0B in_keys(?FRESH1))
     andBool notBool (?HN1_0B in_keys(HRST1))
    [all-path]

  // ---- Entry claim — result = filter_integers(list(VS)) == list(intFilter(0, len, VS, .ValSeq)):
  // the sublist of VS keeping each int-typed element, order preserved. i pre-bound to 0 so the loop
  // invariant folds without a first-iteration unroll. No domain constraint (mixed list; isinstance opaque).
  claim
    <k>
      FuncDef("filter_integers", Params("values"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        Assign(Name("int_type"), Name("int"))
        For(Name("i"), Call(Name("range"), Call(Name("len"), Name("values"))),
          If(Call(Name("isinstance"), (Subscript(Name("values"), Name("i")), Name("int_type"))),
            Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Subscript(Name("values"), Name("i"))))),
            .Stmts))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("filter_integers"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |-> scope(.Map [ "filter_integers" <- ?_:Val ] [ "result" <- ref(?HN2_0:Int) ], parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(intFilter(0, vsLen(VS), VS, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFlat(VS)
    [all-path]
endmodule
