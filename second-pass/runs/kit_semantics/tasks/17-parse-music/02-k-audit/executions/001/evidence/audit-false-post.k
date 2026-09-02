requires "verification.k"

module AUDIT-FALSE-POST
  imports VERIFICATION

  // Fresh reviewer mutation. For satisfying input "o o| .|", the real result
  // is [4, 2, 1]; this deliberately demands [4, 2, 2].
  claim [wrong-quarter-duration]:
    <k> Call(
      Name("parse_music"),
      str(iCons(111,
          iCons(32,
          iCons(111,
          iCons(124,
          iCons(32,
          iCons(46,
          iCons(124, .IntSeq)))))))) , .Exprs)
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
    <heap> .Map => 0 |-> list(
      vCons(4, vCons(2, vCons(2, .ValSeq)))) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
