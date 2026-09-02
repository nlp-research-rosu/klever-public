<mpy>
  <k> loop("value", cons(1, .Ints), searchLoopBody)
       ~> exec(Return(Name("answer")) .Stmts) </k>
  <program> searchProgram </program>
  <input> VList(cons(1, .Ints)) </input>
  <env> "answer" |-> VInt(-1)
        "lst" |-> VList(cons(1, .Ints))
        "value" |-> VInt(99) </env>
  <result> noResult </result>
</mpy>
