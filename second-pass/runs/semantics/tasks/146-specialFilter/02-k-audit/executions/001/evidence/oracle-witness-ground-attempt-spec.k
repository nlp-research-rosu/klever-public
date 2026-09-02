requires "oracle-witness-ground-attempt.k"

module OPPOSITE-DECIMAL-INTERPRETATION-SPEC
  imports OPPOSITE-DECIMAL-INTERPRETATION

  claim [opposite-special-bit]:
    specialBit(12) => 1

  claim [opposite-loop-result]:
    <k> #loop(
          list(intVals(iCons(12, .IntSeq))),
          Name("num"),
          #specialElementBody)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "nums"   |-> list(intVals(iCons(12, .IntSeq)))
        "count"  |-> 0
        "num"    |-> 0
        "digits" |-> str(.IntSeq),
        parent(0))
      0  |-> scope(GLOBAL:Map, parent(-1))
      -1 |-> scope(BUILTINMAP:Map, root)
      =>
      1 |-> scope(
        "nums"   |-> list(intVals(iCons(12, .IntSeq)))
        "count"  |-> 1
        "num"    |-> 12
        "digits" |-> str(decimalCodes(12)),
        parent(0))
      0  |-> scope(GLOBAL, parent(-1))
      -1 |-> scope(BUILTINMAP, root)
    </scopes>
    requires notBool ("str" in_keys(GLOBAL))
      andBool "str" in_keys(BUILTINMAP)
      andBool {BUILTINMAP["str"]}:>Val ==K typeV("str")
endmodule
