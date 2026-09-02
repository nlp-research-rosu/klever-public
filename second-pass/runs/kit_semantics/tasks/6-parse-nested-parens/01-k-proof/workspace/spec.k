requires "verification.k"

module SPEC
  imports VERIFICATION

  // Symbolic circularity for the one program loop. It executes the exact loop
  // body under MPY and summarizes only the resulting scalar/list state.
  claim [scan-loop]:
    <k> #loop(str(CS), Name("char"), loopBody) => .K ... </k>
    <env> L </env>
    <scopes>
      ... L |-> scope(
        ( "paren_string" |-> str(INPUT)
          "depth"  |-> (D:Int => scanDepth(CS, D))
          "deepest" |-> (M:Int => scanDeepest(CS, D, M))
          "depths" |-> ref(H)
          "char" |-> (CH:Str => scanChar(CS, CH)) ),
        parent(0))
      ...
    </scopes>
    <heap>
      ... H |-> list(OUT:ValSeq => scanOutput(CS, D, M, OUT)) ...
    </heap>

  // Required target theorem: load the exact generated program, resolve the
  // named entry point, and execute it for every valid finite input sequence.
  claim [parse-nested-parens]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("parse_nested_parens"), str(CS))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0  |-> scope(
          "parse_nested_parens"
            |-> closureVal("paren_string", solutionBody, 0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(expectedDepths(CS)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validInput(CS)
endmodule
