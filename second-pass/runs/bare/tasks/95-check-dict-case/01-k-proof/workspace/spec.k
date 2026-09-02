requires "verification.k"

module SPEC
  imports VERIFICATION

  // The six aggregate partitions below are exhaustive for the contract:
  // empty; non-string; all-lower; all-upper; mixed lower/upper; and a string
  // that is neither lower nor upper.  Further claims instantiate every prompt
  // example and exercise uncased characters.

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal() </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal())) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("a") StrVal("b")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("a") StrVal("b")))) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("a") StrVal("A") StrVal("B")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("a") StrVal("A") StrVal("B")))) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("a") IntVal(8)) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("a") IntVal(8)))) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("Name") StrVal("Age") StrVal("City")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("Name") StrVal("Age") StrVal("City")))) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("STATE") StrVal("ZIP")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("STATE") StrVal("ZIP")))) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("abc-123") StrVal("z9")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("abc-123") StrVal("z9")))) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("ABC-123") StrVal("Z9")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("ABC-123") StrVal("Z9")))) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("123")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("123")))) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("aA")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(StrVal("aA")))) </result>
    </task>

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(BoolVal(true)) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(BoolVal(true)))) </result>
    </task>
endmodule
