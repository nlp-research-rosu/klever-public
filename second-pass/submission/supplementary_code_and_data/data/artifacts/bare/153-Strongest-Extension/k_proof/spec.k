requires "verification.k"

module SPEC
  imports VERIFICATION

  // The prompt's worked example.
  claim
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> "Slices" </inputClass>
      <inputExtensions>
        strVal("SErviNGSliCes") ; strVal("Cheese") ; strVal("StuFfed")
      </inputExtensions>
      <result> noResult =>
        returned(strVal(("Slices" +String ".") +String
          refStrongest(strVal("SErviNGSliCes") ; strVal("Cheese") ; strVal("StuFfed"))))
      </result>
    </py>

  // Equal strengths retain the earliest extension.  The class name is
  // symbolic here, so this claim covers every class-name string.
  claim
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("AA") ; strVal("Be") ; strVal("CC") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("AA") ; strVal("Be") ; strVal("CC")))) </result>
    </py>

  // A later extension replaces the current one only when its score is
  // strictly greater.
  claim
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("abc") ; strVal("AB") ; strVal("A-b") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("abc") ; strVal("AB") ; strVal("A-b")))) </result>
    </py>

  // Digits and punctuation contribute zero; uppercase contributes +1 and
  // lowercase contributes -1.
  claim
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("a-1") ; strVal("--") ; strVal("A!") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("a-1") ; strVal("--") ; strVal("A!")))) </result>
    </py>

  // Empty and uncased extension names all have score zero, so the empty
  // first element wins the tie.
  claim
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("") ; strVal("123") ; strVal("!") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("") ; strVal("123") ; strVal("!")))) </result>
    </py>

  // Scores may all be negative; the least-negative candidate still wins.
  claim
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("abcd") ; strVal("a") ; strVal("xy") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("abcd") ; strVal("a") ; strVal("xy")))) </result>
    </py>

  // The nonempty-list boundary case.
  claim
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("Zz") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("Zz")))) </result>
    </py>
endmodule
