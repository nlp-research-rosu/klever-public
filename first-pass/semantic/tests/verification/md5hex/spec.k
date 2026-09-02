requires "verification.k"

module MD5HEX-SPEC
  imports MD5HEX-VERIFICATION

  // the chain cools to the opaque digest string; its trusted length property
  // reduces via the lemma (isLen(md5hexCodes(_)) => 32)
  claim
    <k>
      Assign(Name("h"),
        Call(Attribute(Call(Attribute(Name("hashlib"), "md5"),
          (Call(Attribute(str(CS:IntSeq), "encode"), Str("ascii")), .Exprs)), "hexdigest"), .Exprs))
      Assign(Name("n"), Call(Name("len"), Name("h")))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "h" <- str(md5hexCodes(CS)) ] [ "n" <- 32 ], parent(-1))
    </scopes>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
