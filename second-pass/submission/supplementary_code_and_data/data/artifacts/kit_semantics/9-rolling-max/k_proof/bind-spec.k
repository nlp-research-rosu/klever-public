requires "bind-base.k"

module BIND-SPEC
  imports BIND-BASE

  claim [bind-int-name]:
    <k>
      #bindTgt(Name(X:String), I:Int) ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(M:Map => M [ X <- I ], P:Parent) ...
    </scopes>
    requires notBool ("$cells" in_keys(M))
endmodule
