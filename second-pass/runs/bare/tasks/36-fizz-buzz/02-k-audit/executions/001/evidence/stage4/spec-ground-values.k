requires "verification.k"

module SPEC-GROUND-VALUES
  imports VERIFICATION

  claim [digit-77]:
    <fizz>
      <k> .K </k>
      <input> 0 </input>
      <env> .Map </env>
      <result> digitSevens(77) => 2 </result>
    </fizz>

  claim [negative]:
    <fizz>
      <k> .K </k>
      <input> 0 </input>
      <env> .Map </env>
      <result> fizzFrom(0, -100) => 0 </result>
    </fizz>

  claim [zero]:
    <fizz>
      <k> .K </k>
      <input> 0 </input>
      <env> .Map </env>
      <result> fizzFrom(0, 0) => 0 </result>
    </fizz>

  claim [example]:
    <fizz>
      <k> .K </k>
      <input> 0 </input>
      <env> .Map </env>
      <result> fizzFrom(0, 79) => 3 </result>
    </fizz>

  claim [multi-seven]:
    <fizz>
      <k> .K </k>
      <input> 0 </input>
      <env> .Map </env>
      <result> fizzFrom(0, 771) => 37 </result>
    </fizz>

  claim [large]:
    <fizz>
      <k> .K </k>
      <input> 0 </input>
      <env> .Map </env>
      <result> fizzFrom(0, 7778) => 498 </result>
    </fizz>

  claim [end-negative]:
    <fizz>
      <k> .K </k>
      <input> 0 </input>
      <env> .Map </env>
      <result> fizzEnd(-1) => 0 </result>
    </fizz>

  claim [end-positive]:
    <fizz>
      <k> .K </k>
      <input> 0 </input>
      <env> .Map </env>
      <result> fizzEnd(79) => 79 </result>
    </fizz>
endmodule
