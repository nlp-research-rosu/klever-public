requires "verification.k"

module SPEC
  imports VERIFICATION

  // Empty input follows the contract's distinguished None branch.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("string_to_md5"), Str(""))
      =>
      noneV
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => ("string_to_md5" |-> stringToMd5Closure), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  // Every nonempty symbolic string is encoded unchanged and passed to the
  // reference semantics' trusted MD5 oracle before hexdigest is returned.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("string_to_md5"), str(CS))
      =>
      str(md5hexCodes(CS))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => ("string_to_md5" |-> stringToMd5Closure), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires notBool (CS ==K .IntSeq)
endmodule
