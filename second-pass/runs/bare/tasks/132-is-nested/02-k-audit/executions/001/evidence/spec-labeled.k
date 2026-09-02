requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [loop0]:
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

  claim [loop1]:
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

  claim [loop2]:
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

  claim [loop3]:
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

  claim [entry]:
    <k> theSolution ~> start(BS:BString) => .K </k>
    <functions> .Map => .Map </functions>
    <env> .Map => .Map </env>
    <result> noResult => boolVal(scan(0, BS)) </result>
endmodule
