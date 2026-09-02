requires "verification.k"

module AUDIT-PINNING
  imports VERIFICATION

  // The exact submitted Module/FuncDef shape, with the audited exact-body
  // macro, loads to the entry claim's function binding and otherwise leaves
  // the initial configuration unchanged.
  claim [load-submitted-function]:
    <k> #loadAll(
          Module(
            FuncDef("sort_numbers", Params("numbers"), sortNumbersBody)))
      => .K </k>
    <env> 0 </env>
    <scopes> 0  |-> scope(.Map => "sort_numbers" |-> sortNumbersFunction,
                           parent(-1))
             -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
