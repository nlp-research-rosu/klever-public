requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // Loop invariant.  BEST is the first longest string already seen; the
  // remaining N elements update it exactly as firstInSeq specifies.
  claim [longest-loop]:
      <k> forValues("string", seqVal(ID:String, I:Int, N:Int), longestLoopBody)
            ~> exec(Return(Name("result")) .Stmts)
            ~> functionEnd
          => .K </k>
      <env> ("result" |-> strVal(BEST:String)
             "string" |-> OLDSTRING:Value
             REST:Map)
              => ?FINALENV:Map </env>
      <out> noOutput => strVal(firstInSeq(BEST, ID, I, N)) </out>
      requires N >=Int 0

  claim [longest-empty]:
      <k> longestProgram => .K </k>
      <args> seqVal(ID:String, 0, 0) </args>
      <env> .Map => ?FINALENV:Map </env>
      <function> noFunction => ?FINALFUNCTION:Function </function>
      <out> noOutput => noneVal </out>

  claim [longest-nonempty]:
      <k> longestProgram => .K </k>
      <args> seqVal(ID:String, 0, N:Int) </args>
      <env> .Map => ?FINALENV:Map </env>
      <function> noFunction => ?FINALFUNCTION:Function </function>
      <out> noOutput
               => strVal(firstInSeq(stringAt(ID, 0), ID, 0, N)) </out>
      requires N >Int 0

  // Ground claims exercise the ordinary listVal representation used by krun,
  // including the prompt examples and the strict-comparison tie behavior.
  claim [concrete-empty]:
      <k> longestProgram => .K </k>
      <args> listVal(.Values) </args>
      <env> .Map => ?FINALENV:Map </env>
      <function> noFunction => ?FINALFUNCTION:Function </function>
      <out> noOutput => noneVal </out>

  claim [concrete-first-tie]:
      <k> longestProgram => .K </k>
      <args> listVal(strVal("a"), strVal("b"), strVal("c")) </args>
      <env> .Map => ?FINALENV:Map </env>
      <function> noFunction => ?FINALFUNCTION:Function </function>
      <out> noOutput => strVal("a") </out>

  claim [concrete-increasing]:
      <k> longestProgram => .K </k>
      <args> listVal(strVal("a"), strVal("bb"), strVal("ccc")) </args>
      <env> .Map => ?FINALENV:Map </env>
      <function> noFunction => ?FINALFUNCTION:Function </function>
      <out> noOutput => strVal("ccc") </out>

  claim [concrete-late-tie]:
      <k> longestProgram => .K </k>
      <args> listVal(strVal("aa"), strVal("b"), strVal("cc")) </args>
      <env> .Map => ?FINALENV:Map </env>
      <function> noFunction => ?FINALFUNCTION:Function </function>
      <out> noOutput => strVal("aa") </out>
endmodule
