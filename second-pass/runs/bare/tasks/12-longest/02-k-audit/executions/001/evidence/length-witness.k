requires "semantic.k"

module LENGTH-WITNESS
  imports MPY-SEMANTICS

  syntax Stmt ::= "ShowLen" "(" String ")"
  rule <k> ShowLen(S) => .K </k>
       <out> _ => intVal(lengthString(S)) </out>
endmodule
