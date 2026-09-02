requires "verification.k"

module SPEC-VACUITY-FRESH
  imports VERIFICATION

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

  // Fresh false mutation: the real program returns true for BS = "[[]]",
  // while this entry postcondition requires false for every bracket string.
  claim
    <k> theSolution ~> start(BS:BString) => .K </k>
    <functions> .Map => .Map </functions>
    <env> .Map => .Map </env>
    <result> noResult => boolVal(false) </result>
endmodule
