requires "verification-connection.k"

module SPEC-CONNECTION
  imports VERIFICATION-CONNECTION

  claim [fixed-list-loop]:
    <k>
      #loop(
        list(materializeInts(INPUT)),
        Name("x"),
        connectionPositiveLoopBody)
      ~> CONT
      => CONT
    </k>
    <env> LOCAL </env>
    <scopes>
      ...
      LOCAL |-> (
        scope(
          ("l" |-> ARG)
          ("result" |-> ref(ACC_LOC))
          ("x" |-> _OLD_X),
          parent(0))
        =>
        scope(
          ("l" |-> ARG)
          ("result" |-> ref(ACC_LOC))
          ("x" |-> ?_FINAL_X),
          parent(0)))
      ...
    </scopes>
    <heap>
      ...
      ACC_LOC |-> list(
        PREFIX
        =>
        connectionFilter(PREFIX, INPUT))
      ...
    </heap>

  claim [fixed-list-get-positive]:
    <k>
      Call(
        Name("get_positive"),
        list(materializeInts(INPUT)))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "get_positive"
               |-> closureVal(
                     ("l", .ParamNames),
                     connectionGetPositiveBody,
                     0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(connectionFilter(.ValSeq, INPUT))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
