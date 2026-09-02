requires "verification.k"

module SPEC
  imports VERIFICATION

  // For arbitrary accumulator state and arbitrary finite remaining input,
  // execute the real loop and summarize every local it modifies.
  claim [loop-invariant]:
    <k>
      #loop(str(REST:IntSeq), Name("c"), loopBody)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |-> scope(
        "c"            |-> (C0:Str       => lastChar(REST, C0))
        "has_letter"   |-> (FOUND:Bool   => alphaAcc(REST, FOUND))
        "reversed_s"   |-> (str(REV:IntSeq)
                            => str(revISAcc(REST, REV)))
        "s"            |-> str(INPUT:IntSeq)
        "swapped"      |-> (str(SWAPPED:IntSeq)
                            => str(toggleAcc(REST, SWAPPED))),
        parent(0))
      ...
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Exact module load, binding, function body, argument evaluation, loop,
  // return, frame pop, and assignment for every modeled finite string.
  claim [solve-full-domain]:
    <k>
      #loadAll(Module(
        FuncDef("solve", Params("s"), solveBody)
        Assign(Name("answer"), Call(Name("solve"), str(INPUT:IntSeq)))
        .Stmts))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0  |-> scope(
               "answer" |-> solveResult(INPUT)
               "solve"  |-> ?SOLVE:Val,
               parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
