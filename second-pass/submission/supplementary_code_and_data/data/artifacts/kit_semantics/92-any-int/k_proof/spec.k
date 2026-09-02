requires "verification.k"

module SPEC
  imports VERIFICATION

  // These eight claims cover every combination accepted by isinstance(_, int)
  // in the supplied semantics: unbounded Int values and both Bool values.
  claim [int-int-int]:
    <k> AnyIntCall(X:Int, Y:Int, Z:Int) => ?R:Bool </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool anySum(X, Y, Z)

  claim [int-int-bool]:
    <k> AnyIntCall(X:Int, Y:Int, Z:Bool) => ?R:Bool </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool anySum(X, Y, boolAsInt(Z))

  claim [int-bool-int]:
    <k> AnyIntCall(X:Int, Y:Bool, Z:Int) => ?R:Bool </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool anySum(X, boolAsInt(Y), Z)

  claim [int-bool-bool]:
    <k> AnyIntCall(X:Int, Y:Bool, Z:Bool) => ?R:Bool </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool anySum(X, boolAsInt(Y), boolAsInt(Z))

  claim [bool-int-int]:
    <k> AnyIntCall(X:Bool, Y:Int, Z:Int) => ?R:Bool </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool anySum(boolAsInt(X), Y, Z)

  claim [bool-int-bool]:
    <k> AnyIntCall(X:Bool, Y:Int, Z:Bool) => ?R:Bool </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool anySum(boolAsInt(X), Y, boolAsInt(Z))

  claim [bool-bool-int]:
    <k> AnyIntCall(X:Bool, Y:Bool, Z:Int) => ?R:Bool </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool anySum(boolAsInt(X), boolAsInt(Y), Z)

  claim [bool-bool-bool]:
    <k> AnyIntCall(X:Bool, Y:Bool, Z:Bool) => ?R:Bool </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool anySum(boolAsInt(X), boolAsInt(Y), boolAsInt(Z))

  // A Float is not an int.  Short-circuiting means later arguments remain
  // arbitrary values once the first failing isinstance check is reached.
  claim [float-any-any]:
    <k> AnyIntCall(X:Float, Y:Val, Z:Val) => false </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [int-float-any]:
    <k> AnyIntCall(X:Int, Y:Float, Z:Val) => false </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [bool-float-any]:
    <k> AnyIntCall(X:Bool, Y:Float, Z:Val) => false </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [int-int-float]:
    <k> AnyIntCall(X:Int, Y:Int, Z:Float) => false </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [int-bool-float]:
    <k> AnyIntCall(X:Int, Y:Bool, Z:Float) => false </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [bool-int-float]:
    <k> AnyIntCall(X:Bool, Y:Int, Z:Float) => false </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [bool-bool-float]:
    <k> AnyIntCall(X:Bool, Y:Bool, Z:Float) => false </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
