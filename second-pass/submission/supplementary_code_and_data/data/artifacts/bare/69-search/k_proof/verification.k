requires "verification-core.k"

module VERIFICATION
  imports VERIFICATION-CORE

  // Derived summary rule.  loop-lemma-spec.k proves this exact reachability
  // step against the raw small-step semantics before this module is compiled.
  rule <k> loop("value", IS, searchLoopBody)
            ~> exec(Return(Name("answer")) .Stmts) => .K </k>
       <program> searchProgram </program>
       <input> VList(L) </input>
       <env> ("answer" |-> VInt(A)
              "lst" |-> VList(L)
              "value" |-> VInt(_PREV)) => .Map </env>
       <result> noResult => VInt(scan(L, IS, A)) </result>
       [priority(40)]
endmodule
