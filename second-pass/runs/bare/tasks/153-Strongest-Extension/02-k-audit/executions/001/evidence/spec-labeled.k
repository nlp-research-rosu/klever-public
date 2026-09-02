requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [case01]:
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

  claim [case02]:
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("AA") ; strVal("Be") ; strVal("CC") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("AA") ; strVal("Be") ; strVal("CC")))) </result>
    </py>

  claim [case03]:
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("abc") ; strVal("AB") ; strVal("A-b") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("abc") ; strVal("AB") ; strVal("A-b")))) </result>
    </py>

  claim [case04]:
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("a-1") ; strVal("--") ; strVal("A!") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("a-1") ; strVal("--") ; strVal("A!")))) </result>
    </py>

  claim [case05]:
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("") ; strVal("123") ; strVal("!") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("") ; strVal("123") ; strVal("!")))) </result>
    </py>

  claim [case06]:
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> C:String </inputClass>
      <inputExtensions> strVal("abcd") ; strVal("a") ; strVal("xy") </inputExtensions>
      <result> noResult => returned(strVal((C +String ".") +String
        refStrongest(strVal("abcd") ; strVal("a") ; strVal("xy")))) </result>
    </py>

  claim [case07]:
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
