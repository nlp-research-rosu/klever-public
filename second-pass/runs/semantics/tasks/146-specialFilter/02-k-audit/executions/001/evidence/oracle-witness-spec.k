requires "oracle-witness.k"

module OPPOSITE-DECIMAL-INTERPRETATION-SPEC
  imports OPPOSITE-DECIMAL-INTERPRETATION

  // This executes the actual element body under the candidate's proof syntax,
  // without importing the candidate's derived loop-summary rule. The admitted
  // opposite interpretation proves that every symbolic N > 10 increments
  // count. N=12 is a false concrete instance of that symbolic conclusion.
  claim [opposite-loop-result]:
    <k> #loop(
          list(intVals(iCons(N:Int, .IntSeq))),
          Name("num"),
          #specialElementBody)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "nums"   |-> list(intVals(iCons(N, .IntSeq)))
        "count"  |-> 0
        "num"    |-> 0
        "digits" |-> str(.IntSeq),
        parent(0))
      0  |-> scope(GLOBAL:Map, parent(-1))
      -1 |-> scope(BUILTINMAP:Map, root)
      =>
      1 |-> scope(
        "nums"   |-> list(intVals(iCons(N, .IntSeq)))
        "count"  |-> 1
        "num"    |-> N
        "digits" |-> str(decimalCodes(N)),
        parent(0))
      0  |-> scope(GLOBAL, parent(-1))
      -1 |-> scope(BUILTINMAP, root)
    </scopes>
    requires N >Int 10
      andBool notBool ("str" in_keys(GLOBAL))
      andBool "str" in_keys(BUILTINMAP)
      andBool {BUILTINMAP["str"]}:>Val ==K typeV("str")
endmodule
