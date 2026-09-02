requires "verification.k"

module AUDIT-GROUND-SPEC
  imports VERIFICATION

  // Satisfying entry state: CS = .IntSeq, whose claimed result is [].
  claim [parse-empty]:
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
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Ground substitution "o o| .|" into musicResult(CS): [4, 2, 1].
  claim [parse-short]:
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
      vCons(4, vCons(2, vCons(1, .ValSeq)))) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // A fully ground state satisfying the loop claim's precondition.
  claim [scan-loop-empty]:
    <k> #loop(str(.IntSeq), Name("char"), parseMusicCharBody)
      => .K ... </k>
    <env> 1 </env>
    <scopes> ... 1 |-> scope(
        ("music_string" |-> str(.IntSeq)
         "result"       |-> ref(2)
         "current"      |-> 0
         "char"         |-> str(.IntSeq))
        =>
        ("music_string" |-> str(.IntSeq)
         "result"       |-> ref(2)
         "current"      |-> 0
         "char"         |-> ?FINALCHAR:Str),
        parent(-1)) ... </scopes>
    <heap> ... 2 |-> list(.ValSeq => .ValSeq) ... </heap>
endmodule
