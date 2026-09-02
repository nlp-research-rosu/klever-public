requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop invariants, one for each reference-automaton state.  ORIG is retained
  // in the Python local environment; CUR is the previous loop character (or
  // the dummy empty value before the first iteration).  Both are irrelevant
  // to the suffix result, which is exactly scan(State, BS).
  claim
    <k> iterate("bracket", BS:BString, loopBody)
         ~> (Return(Bool(false)) .Stmts) => .K </k>
    <functions>
      "is_nested" |-> function(Params("string"), solutionBody) => .Map
    </functions>
    <env>
      ( "string"  |-> strVal(_ORIG:BString)
        "state"   |-> intVal(0)
        "bracket" |-> strVal(_CUR:BString) ) => .Map
    </env>
    <result> noResult => boolVal(scan(0, BS)) </result>

  claim
    <k> iterate("bracket", BS:BString, loopBody)
         ~> (Return(Bool(false)) .Stmts) => .K </k>
    <functions>
      "is_nested" |-> function(Params("string"), solutionBody) => .Map
    </functions>
    <env>
      ( "string"  |-> strVal(_ORIG:BString)
        "state"   |-> intVal(1)
        "bracket" |-> strVal(_CUR:BString) ) => .Map
    </env>
    <result> noResult => boolVal(scan(1, BS)) </result>

  claim
    <k> iterate("bracket", BS:BString, loopBody)
         ~> (Return(Bool(false)) .Stmts) => .K </k>
    <functions>
      "is_nested" |-> function(Params("string"), solutionBody) => .Map
    </functions>
    <env>
      ( "string"  |-> strVal(_ORIG:BString)
        "state"   |-> intVal(2)
        "bracket" |-> strVal(_CUR:BString) ) => .Map
    </env>
    <result> noResult => boolVal(scan(2, BS)) </result>

  claim
    <k> iterate("bracket", BS:BString, loopBody)
         ~> (Return(Bool(false)) .Stmts) => .K </k>
    <functions>
      "is_nested" |-> function(Params("string"), solutionBody) => .Map
    </functions>
    <env>
      ( "string"  |-> strVal(_ORIG:BString)
        "state"   |-> intVal(3)
        "bracket" |-> strVal(_CUR:BString) ) => .Map
    </env>
    <result> noResult => boolVal(scan(3, BS)) </result>

  // Universal end-to-end functional correctness for every string admitted by
  // the prompt (that is, every finite BString of left/right brackets).
  claim
    <k> theSolution ~> start(BS:BString) => .K </k>
    <functions> .Map => .Map </functions>
    <env> .Map => .Map </env>
    <result> noResult => boolVal(scan(0, BS)) </result>
endmodule
