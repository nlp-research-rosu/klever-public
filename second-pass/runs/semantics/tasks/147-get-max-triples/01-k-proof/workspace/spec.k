requires "verification.k"

module SPEC
  imports VERIFICATION

  // a_i = i^2-i+1 is 1, 1, 0 modulo 3 for i = 0, 1, 2 modulo 3.
  claim [residue-0]:
    <k>
      pyMod((3 *Int Q:Int) *Int (3 *Int Q)
            -Int (3 *Int Q) +Int 1, 3)
      => 1
    </k>

  claim [residue-1]:
    <k>
      pyMod((3 *Int Q:Int +Int 1) *Int (3 *Int Q +Int 1)
            -Int (3 *Int Q +Int 1) +Int 1, 3)
      => 1
    </k>

  claim [residue-2]:
    <k>
      pyMod((3 *Int Q:Int +Int 2) *Int (3 *Int Q +Int 2)
            -Int (3 *Int Q +Int 2) +Int 1, 3)
      => 0
    </k>

  // Execute the translated function for an arbitrary positive n.  The
  // right-hand side is the independently stated residue-counting model:
  // choose all three indices from the zero class or all three from the one
  // class.
  claim [get-max-triples-correct]:
    <k>
      Call(Name("get_max_triples"), (Int(N:Int), .Exprs))
      => tripleCount(N)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "get_max_triples" |-> closureVal(
          ("n", .ParamNames), getMaxTriplesBody, 0),
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
    requires N >Int 0
endmodule
