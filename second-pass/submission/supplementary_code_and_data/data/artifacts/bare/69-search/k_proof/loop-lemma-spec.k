requires "verification-core.k"

module LOOP-LEMMA-SPEC
  imports VERIFICATION-CORE

  // Inductive loop invariant after at least one iteration.  PREV is
  // intentionally irrelevant: the next semantic loop step overwrites it.
  claim [loop-invariant]:
        <k> loop("value", IS, searchLoopBody)
             ~> exec(Return(Name("answer")) .Stmts) => .K </k>
        <program> searchProgram </program>
        <input> VList(L) </input>
        <env> ("answer" |-> VInt(A)
               "lst" |-> VList(L)
               "value" |-> VInt(_PREV)) => .Map </env>
        <result> noResult => VInt(scan(L, IS, A)) </result>
endmodule
