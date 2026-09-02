requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [label(empty)]:
    <py>
      <k> #load(solutionProgram) => .K </k>
      <input> "" </input>
      <functions>
        .Map => "string_to_md5" |-> fn("text", solutionBody)
      </functions>
      <env> .Map => "text" |-> pyString("") </env>
      <result> noResult => pyNone </result>
    </py>

  claim [label(nonempty-symbolic)]:
    <py>
      <k> #load(solutionProgram) => .K </k>
      <input> S:String </input>
      <functions>
        .Map => "string_to_md5" |-> fn("text", solutionBody)
      </functions>
      <env> .Map => "text" |-> pyString(S) </env>
      <result> noResult => expectedMd5(S) </result>
    </py>
    requires S =/=String ""

  claim [label(prompt-example)]:
    <py>
      <k> #load(solutionProgram) => .K </k>
      <input> "Hello world" </input>
      <functions>
        .Map => "string_to_md5" |-> fn("text", solutionBody)
      </functions>
      <env> .Map => "text" |-> pyString("Hello world") </env>
      <result>
        noResult => pyString("3e25960a79dbc69b674cd4ec67a72c62")
      </result>
    </py>

  claim [label(unicode-utf8)]:
    <py>
      <k> #load(solutionProgram) => .K </k>
      <input> "π" </input>
      <functions>
        .Map => "string_to_md5" |-> fn("text", solutionBody)
      </functions>
      <env> .Map => "text" |-> pyString("π") </env>
      <result>
        noResult => pyString("31bf0b12546409e15021243132fc7574")
      </result>
    </py>

  claim [label(multiblock-padding)]:
    <py>
      <k> #load(solutionProgram) => .K </k>
      <input>
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
      </input>
      <functions>
        .Map => "string_to_md5" |-> fn("text", solutionBody)
      </functions>
      <env>
        .Map => "text" |-> pyString(
          "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
      </env>
      <result>
        noResult => pyString("b15af9cdabbaea0516866a33d8fd0f98")
      </result>
    </py>
endmodule
