requires "fixed-verification.k"

module POP-GROUND
  imports FIXED-VERIFICATION

  claim [only-frame]:
    <k> #pop => true </k>
    <ret> retV(true) => noRet </ret>
    <stack> ListItem(frame(.K, 0, 1)) .List => .List </stack>
    <env> 1 => 0 </env>
    <scopes>
      1 |-> scope(.Map, parent(0))
      =>
      .Map
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>

  claim [preserve-other-frames]:
    <k> #pop => false </k>
    <ret> retV(false) => noRet </ret>
    <stack>
      ListItem(frame(.K, 0, 2))
      ListItem(frame(true, -1, 7))
      =>
      ListItem(frame(true, -1, 7))
    </stack>
    <env> 2 => 0 </env>
    <scopes>
      2 |-> scope("x" |-> 9, parent(0))
      0 |-> scope("g" |-> true, root)
      -1 |-> scope(.Map, root)
      =>
      0 |-> scope("g" |-> true, root)
      -1 |-> scope(.Map, root)
    </scopes>
    <scopeLoc> 3 => 2 </scopeLoc>
endmodule
