requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the real result has sort Float, not None.
  claim [triangle-area-false-result]:
    <k>
      (#loadAll(Module(
        FuncDef("triangle_area", Params("a", "h"),
          Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0))))))
      ~> Call(Name("triangle_area"), (A:Int, H:Int, .Exprs)))
      => noneV ~> .K
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
