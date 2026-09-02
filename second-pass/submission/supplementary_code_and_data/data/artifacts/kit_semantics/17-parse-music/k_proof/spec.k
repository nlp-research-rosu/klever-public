requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [scan-loop]:
    <k> #loop(str(CS:IntSeq), Name("char"), parseMusicCharBody)
      => .K ... </k>
    <env> L:Int </env>
    <scopes> ... L |-> scope(
        ("music_string" |-> INPUT:Str
         "result"       |-> ref(H:Int)
         "current"      |-> CUR:Int
         "char"         |-> OLDCHAR:Str)
        =>
        ("music_string" |-> INPUT
         "result"       |-> ref(H)
         "current"      |-> scanCurrent(CS, CUR)
         "char"         |-> ?FINALCHAR:Str),
        P:Parent) ... </scopes>
    <heap> ... H |-> list(ACC:ValSeq => scanResult(CS, CUR, ACC)) ... </heap>

  claim [parse-music]:
    <k> Call(Name("parse_music"), str(CS:IntSeq) , .Exprs)
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
    <heap> .Map => 0 |-> list(musicResult(CS)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
