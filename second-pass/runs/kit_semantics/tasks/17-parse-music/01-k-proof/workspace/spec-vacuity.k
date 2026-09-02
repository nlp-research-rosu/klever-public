requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable witness music_string == "".
  claim [false-empty-result]:
    <k> Call(Name("parse_music"), str(.IntSeq) , .Exprs)
      => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "parse_music" |-> closureVal(
          "music_string" , .ParamNames,
          parseMusicBody,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(99, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
