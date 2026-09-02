requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [case-01-empty]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal() </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal())) </result>
    </task>

  claim [case-02-lower]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("a") StrVal("b")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("a") StrVal("b")))) </result>
    </task>

  claim [case-03-mixed]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("a") StrVal("A") StrVal("B")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("a") StrVal("A") StrVal("B")))) </result>
    </task>

  claim [case-04-int]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("a") IntVal(8)) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("a") IntVal(8)))) </result>
    </task>

  claim [case-05-title]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("Name") StrVal("Age") StrVal("City")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("Name") StrVal("Age") StrVal("City")))) </result>
    </task>

  claim [case-06-upper]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("STATE") StrVal("ZIP")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("STATE") StrVal("ZIP")))) </result>
    </task>

  claim [case-07-lower-uncased]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("abc-123") StrVal("z9")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("abc-123") StrVal("z9")))) </result>
    </task>

  claim [case-08-upper-uncased]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("ABC-123") StrVal("Z9")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("ABC-123") StrVal("Z9")))) </result>
    </task>

  claim [case-09-uncased]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("123")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("123")))) </result>
    </task>

  claim [case-10-single-mixed]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("aA")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("aA")))) </result>
    </task>

  claim [case-11-bool]:
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(BoolVal(true)) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(BoolVal(true)))) </result>
    </task>
endmodule
