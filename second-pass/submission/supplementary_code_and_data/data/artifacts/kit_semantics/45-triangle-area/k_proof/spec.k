requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [triangle-area-int-int]:
    <k>
      (#loadAll(Module(
        FuncDef("triangle_area", Params("a", "h"),
          Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))))))
      ~> Call(Name("triangle_area"), (A:Int, H:Int, .Exprs)))
      => intFloatDiv(A *Int H, 2.0) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "triangle_area" |-> closureVal(
             ("a", "h"),
             Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))),
             0),
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

  claim [triangle-area-int-float]:
    <k>
      (#loadAll(Module(
        FuncDef("triangle_area", Params("a", "h"),
          Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))))))
      ~> Call(Name("triangle_area"), (A:Int, H:Float, .Exprs)))
      => divF(mulF(intToF(A), H), 2.0) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "triangle_area" |-> closureVal(
             ("a", "h"),
             Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))),
             0),
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

  claim [triangle-area-float-int]:
    <k>
      (#loadAll(Module(
        FuncDef("triangle_area", Params("a", "h"),
          Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))))))
      ~> Call(Name("triangle_area"), (A:Float, H:Int, .Exprs)))
      => divF(mulF(A, intToF(H)), 2.0) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "triangle_area" |-> closureVal(
             ("a", "h"),
             Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))),
             0),
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

  claim [triangle-area-float-float]:
    <k>
      (#loadAll(Module(
        FuncDef("triangle_area", Params("a", "h"),
          Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))))))
      ~> Call(Name("triangle_area"), (A:Float, H:Float, .Exprs)))
      => divF(mulF(A, H), 2.0) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "triangle_area" |-> closureVal(
             ("a", "h"),
             Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))),
             0),
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
endmodule
