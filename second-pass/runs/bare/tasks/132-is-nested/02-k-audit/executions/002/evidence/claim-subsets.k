requires "verification.k"

// Reviewer-authored cumulative subsets. Each module adds the next real claim
// dependency: loop state 3 is self-contained; state 2 uses state 3; state 1
// uses states 2 and 3; state 0 uses states 1, 2, and 3.

module AUDIT-SPEC-LOOP3
  imports VERIFICATION

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
endmodule

module AUDIT-SPEC-LOOP2
  imports VERIFICATION

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
endmodule

module AUDIT-SPEC-LOOP1
  imports VERIFICATION

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
endmodule

module AUDIT-SPEC-LOOP0
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
endmodule
