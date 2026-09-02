requires "spec.k"

module AUDIT-VACUITY
  imports SPEC

  // The exact submitted function returns false on the empty all-float list.
  // This fresh mutation deliberately requires true instead.
  claim [false-empty-result]:
    <k> #loadAll(Module(
          ImportFrom("typing", "List")
          FuncDef("has_close_elements", Params("numbers", "threshold"),
                  HC-FUNCTION-BODY)))
         ~> Call(Name("has_close_elements"), list(.ValSeq), 0.5)
        => ?R:Bool </k>
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
    requires allFloatVS(.ValSeq)
    ensures ?R ==Bool true
endmodule
