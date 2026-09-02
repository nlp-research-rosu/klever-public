requires "unicode-case.k"

module MPY-SYNTAX
  imports STRING-SYNTAX

  syntax Module ::= "Module" "(" Stmts ")"

  syntax Stmts ::= Stmt
                 | Stmt Stmts

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Str" "(" String ")"
                | "Name" "(" String ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports MAP
  imports PYTHON-UNICODE-CASE
  imports STRING

  // Values needed by this program.  Functions retain their untranslated AST
  // body, and a method value retains both its name and its receiver.
  syntax Value ::= strVal(String)
                 | function(Params, Stmts)
                 | boundStringMethod(String, String)
  syntax KResult ::= Value

  syntax KItem ::= "#invoke" "(" String "," Value ")"
                 | "#attribute" "(" String ")"
                 | "#callNoArgs"
                 | "#return"
                 | "#endCall"

  configuration
    <mpy>
      <k> $PGM:Module </k>
      <arg> $ARG:String </arg>
      <functions> .Map </functions>
      <env> .Map </env>
    </mpy>

  // Loading a module installs its definitions, then invokes the HumanEval
  // entry point on the symbolic/configuration-provided argument.
  rule <k> Module(BODY) => BODY ~> #invoke("flip_case", strVal(ARG)) ...</k>
       <arg> ARG </arg>

  rule <k> S:Stmt REST:Stmts => S ~> REST ...</k>

  rule <k> FuncDef(F, PARAMS, BODY) => .K ...</k>
       <functions> FUNS => FUNS[F <- function(PARAMS, BODY)] </functions>

  rule <k> #invoke(F, V) => BODY ~> #endCall ...</k>
       <functions>... F |-> function(Params(P:String), BODY) ...</functions>
       <env> .Map => P |-> V </env>

  rule <k> Return(E) => E ~> #return ...</k>

  rule <k> Name(N) => V ...</k>
       <env>... N |-> V ...</env>

  rule <k> Str(S) => strVal(S) ...</k>

  rule <k> Attribute(E, NAME) => E ~> #attribute(NAME) ...</k>
  rule <k> strVal(S) ~> #attribute(NAME)
        => boundStringMethod(NAME, S) ...</k>

  rule <k> Call(F, .Exprs) => F ~> #callNoArgs ...</k>
  rule <k> boundStringMethod("swapcase", S) ~> #callNoArgs
        => strVal(pySwapCase(S)) ...</k>

  rule <k> V:Value ~> #return ~> #endCall => V ...</k>
       <env> _ => .Map </env>

  // Python's str.swapcase is defined character-by-character.  pySwapChar is
  // supplied by the generated helper module, including every mapping (and
  // multi-code-point expansion) in the local CPython Unicode database.
  syntax String ::= pySwapCase(String) [function]
  syntax Int ::= utf8CharLen(String) [function, total]

  rule pySwapCase("") => ""
  rule pySwapCase(S) =>
         pySwapChar(substrString(S, 0, utf8CharLen(S)))
         +String pySwapCase(
           substrString(S, utf8CharLen(S), lengthString(S)))
    requires S =/=String ""

  // K 7.1's String hook exposes non-ASCII text as UTF-8 bytes.  Decode the
  // leading-byte width so each pySwapChar call still receives one Python
  // Unicode scalar value (encoded as one to four K String bytes).
  rule utf8CharLen(S) => 1
    requires ordChar(substrString(S, 0, 1)) <Int 128
  rule utf8CharLen(S) => 2
    requires 192 <=Int ordChar(substrString(S, 0, 1))
     andBool ordChar(substrString(S, 0, 1)) <Int 224
  rule utf8CharLen(S) => 3
    requires 224 <=Int ordChar(substrString(S, 0, 1))
     andBool ordChar(substrString(S, 0, 1)) <Int 240
  rule utf8CharLen(S) => 4
    requires 240 <=Int ordChar(substrString(S, 0, 1))
     andBool ordChar(substrString(S, 0, 1)) <Int 248
  rule utf8CharLen(_) => 1 [owise]

endmodule
