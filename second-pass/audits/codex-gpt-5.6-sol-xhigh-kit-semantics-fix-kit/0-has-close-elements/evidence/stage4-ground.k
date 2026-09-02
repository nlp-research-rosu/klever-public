requires "spec.k"

module AUDIT-GROUND
  imports SPEC

  claim [close-witness]:
    <k> #loadAll(Module(
          ImportFrom("typing", "List")
          FuncDef("has_close_elements", Params("numbers", "threshold"),
                  HC-FUNCTION-BODY)))
         ~> Call(Name("has_close_elements"),
                 list(vCons(1.0, vCons(1.125, .ValSeq))), 0.25)
        => true </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => ?MODULE:Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [strict-boundary-witness]:
    <k> #loadAll(Module(
          ImportFrom("typing", "List")
          FuncDef("has_close_elements", Params("numbers", "threshold"),
                  HC-FUNCTION-BODY)))
         ~> Call(Name("has_close_elements"),
                 list(vCons(1.0, vCons(1.5, .ValSeq))), 0.5)
        => false </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => ?MODULE:Map, parent(-1))
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
