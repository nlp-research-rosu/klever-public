requires "verification.k"

module SPEC
  imports VERIFICATION

  // The three examples from prompt.py.
  claim [example-one]: <k> boot => .K </k>
        <program> searchProgram </program>
        <input> VList(cons(4, cons(1, cons(2, cons(2, cons(3, cons(1, .Ints))))))) </input>
        <env> .Map </env>
        <result> noResult => VInt(2) </result>

  claim [example-two]: <k> boot => .K </k>
        <program> searchProgram </program>
        <input> VList(cons(1, cons(2, cons(2, cons(3, cons(3, cons(3,
                 cons(4, cons(4, cons(4, .Ints)))))))))) </input>
        <env> .Map </env>
        <result> noResult => VInt(3) </result>

  claim [example-three]: <k> boot => .K </k>
        <program> searchProgram </program>
        <input> VList(cons(5, cons(5, cons(4, cons(4, cons(4, .Ints)))))) </input>
        <env> .Map </env>
        <result> noResult => VInt(-1) </result>

  // Universal functional-correctness theorem for every non-empty integer
  // list (and hence the prompt's positive-list domain).  searchSpec is the
  // recursive maximum-by-frequency contract.
  claim [functional-correctness]: <k> boot => .K </k>
        <program> searchProgram </program>
        <input> VList(cons(H, T)) </input>
        <env> .Map </env>
        <result> noResult => VInt(searchSpec(cons(H, T))) </result>
endmodule
