requires "verification-body-mutant.k"

module SPECIALFILTER-BODY-MUTANT-SPEC
  imports SPECIALFILTER-VERIFICATION-LOOP

  claim [specialfilter-loop-original-obligation]:
    <k> #loop(list(intVals(NS:IntSeq)), Name("num"), #specialElementBody)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "nums"   |-> list(intVals(ALL:IntSeq))
        "count"  |-> C:Int
        "num"    |-> OLDNUM:Int
        "digits" |-> OLDDIGITS:Str,
        parent(0))
      0  |-> scope(GLOBAL:Map, parent(-1))
      -1 |-> scope(BUILTINMAP:Map, root)
      =>
      1 |-> scope(
        "nums"   |-> list(intVals(ALL))
        "count"  |-> C +Int specialCount(NS)
        "num"    |-> finalNum(OLDNUM, NS)
        "digits" |-> finalDigits(OLDDIGITS, NS),
        parent(0))
      0  |-> scope(GLOBAL, parent(-1))
      -1 |-> scope(BUILTINMAP, root)
    </scopes>
    requires notBool ("str" in_keys(GLOBAL))
      andBool "str" in_keys(BUILTINMAP)
      andBool {BUILTINMAP["str"]}:>Val ==K typeV("str")
endmodule
