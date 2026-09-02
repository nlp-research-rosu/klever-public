requires "verification.k"

module BF-SPEC
  imports VERIFICATION

  claim
    <k> verifyBF("Mercury", "Mercury") => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => "Mercury" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Mercury", "Venus") => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => "Venus" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Mercury", "Earth") => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => "Earth" </planet2>
    <result> noResult => tupleValue("Venus") </result>

  claim
    <k> verifyBF("Mercury", "Mars") => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => "Mars" </planet2>
    <result> noResult => tupleValue("Venus", "Earth") </result>

  claim
    <k> verifyBF("Mercury", "Jupiter") => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => "Jupiter" </planet2>
    <result> noResult => tupleValue("Venus", "Earth", "Mars") </result>

  claim
    <k> verifyBF("Mercury", "Saturn") => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => "Saturn" </planet2>
    <result> noResult => tupleValue("Venus", "Earth", "Mars", "Jupiter") </result>

  claim
    <k> verifyBF("Mercury", "Uranus") => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => "Uranus" </planet2>
    <result> noResult => tupleValue("Venus", "Earth", "Mars", "Jupiter", "Saturn") </result>

  claim
    <k> verifyBF("Mercury", "Neptune") => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => "Neptune" </planet2>
    <result> noResult => tupleValue("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Venus", "Mercury") => .K </k>
    <planet1> "" => "Venus" </planet1>
    <planet2> "" => "Mercury" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Venus", "Venus") => .K </k>
    <planet1> "" => "Venus" </planet1>
    <planet2> "" => "Venus" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Venus", "Earth") => .K </k>
    <planet1> "" => "Venus" </planet1>
    <planet2> "" => "Earth" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Venus", "Mars") => .K </k>
    <planet1> "" => "Venus" </planet1>
    <planet2> "" => "Mars" </planet2>
    <result> noResult => tupleValue("Earth") </result>

  claim
    <k> verifyBF("Venus", "Jupiter") => .K </k>
    <planet1> "" => "Venus" </planet1>
    <planet2> "" => "Jupiter" </planet2>
    <result> noResult => tupleValue("Earth", "Mars") </result>

  claim
    <k> verifyBF("Venus", "Saturn") => .K </k>
    <planet1> "" => "Venus" </planet1>
    <planet2> "" => "Saturn" </planet2>
    <result> noResult => tupleValue("Earth", "Mars", "Jupiter") </result>

  claim
    <k> verifyBF("Venus", "Uranus") => .K </k>
    <planet1> "" => "Venus" </planet1>
    <planet2> "" => "Uranus" </planet2>
    <result> noResult => tupleValue("Earth", "Mars", "Jupiter", "Saturn") </result>

  claim
    <k> verifyBF("Venus", "Neptune") => .K </k>
    <planet1> "" => "Venus" </planet1>
    <planet2> "" => "Neptune" </planet2>
    <result> noResult => tupleValue("Earth", "Mars", "Jupiter", "Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Earth", "Mercury") => .K </k>
    <planet1> "" => "Earth" </planet1>
    <planet2> "" => "Mercury" </planet2>
    <result> noResult => tupleValue("Venus") </result>

  claim
    <k> verifyBF("Earth", "Venus") => .K </k>
    <planet1> "" => "Earth" </planet1>
    <planet2> "" => "Venus" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Earth", "Earth") => .K </k>
    <planet1> "" => "Earth" </planet1>
    <planet2> "" => "Earth" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Earth", "Mars") => .K </k>
    <planet1> "" => "Earth" </planet1>
    <planet2> "" => "Mars" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Earth", "Jupiter") => .K </k>
    <planet1> "" => "Earth" </planet1>
    <planet2> "" => "Jupiter" </planet2>
    <result> noResult => tupleValue("Mars") </result>

  claim
    <k> verifyBF("Earth", "Saturn") => .K </k>
    <planet1> "" => "Earth" </planet1>
    <planet2> "" => "Saturn" </planet2>
    <result> noResult => tupleValue("Mars", "Jupiter") </result>

  claim
    <k> verifyBF("Earth", "Uranus") => .K </k>
    <planet1> "" => "Earth" </planet1>
    <planet2> "" => "Uranus" </planet2>
    <result> noResult => tupleValue("Mars", "Jupiter", "Saturn") </result>

  claim
    <k> verifyBF("Earth", "Neptune") => .K </k>
    <planet1> "" => "Earth" </planet1>
    <planet2> "" => "Neptune" </planet2>
    <result> noResult => tupleValue("Mars", "Jupiter", "Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Mars", "Mercury") => .K </k>
    <planet1> "" => "Mars" </planet1>
    <planet2> "" => "Mercury" </planet2>
    <result> noResult => tupleValue("Venus", "Earth") </result>

  claim
    <k> verifyBF("Mars", "Venus") => .K </k>
    <planet1> "" => "Mars" </planet1>
    <planet2> "" => "Venus" </planet2>
    <result> noResult => tupleValue("Earth") </result>

  claim
    <k> verifyBF("Mars", "Earth") => .K </k>
    <planet1> "" => "Mars" </planet1>
    <planet2> "" => "Earth" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Mars", "Mars") => .K </k>
    <planet1> "" => "Mars" </planet1>
    <planet2> "" => "Mars" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Mars", "Jupiter") => .K </k>
    <planet1> "" => "Mars" </planet1>
    <planet2> "" => "Jupiter" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Mars", "Saturn") => .K </k>
    <planet1> "" => "Mars" </planet1>
    <planet2> "" => "Saturn" </planet2>
    <result> noResult => tupleValue("Jupiter") </result>

  claim
    <k> verifyBF("Mars", "Uranus") => .K </k>
    <planet1> "" => "Mars" </planet1>
    <planet2> "" => "Uranus" </planet2>
    <result> noResult => tupleValue("Jupiter", "Saturn") </result>

  claim
    <k> verifyBF("Mars", "Neptune") => .K </k>
    <planet1> "" => "Mars" </planet1>
    <planet2> "" => "Neptune" </planet2>
    <result> noResult => tupleValue("Jupiter", "Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Jupiter", "Mercury") => .K </k>
    <planet1> "" => "Jupiter" </planet1>
    <planet2> "" => "Mercury" </planet2>
    <result> noResult => tupleValue("Venus", "Earth", "Mars") </result>

  claim
    <k> verifyBF("Jupiter", "Venus") => .K </k>
    <planet1> "" => "Jupiter" </planet1>
    <planet2> "" => "Venus" </planet2>
    <result> noResult => tupleValue("Earth", "Mars") </result>

  claim
    <k> verifyBF("Jupiter", "Earth") => .K </k>
    <planet1> "" => "Jupiter" </planet1>
    <planet2> "" => "Earth" </planet2>
    <result> noResult => tupleValue("Mars") </result>

  claim
    <k> verifyBF("Jupiter", "Mars") => .K </k>
    <planet1> "" => "Jupiter" </planet1>
    <planet2> "" => "Mars" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Jupiter", "Jupiter") => .K </k>
    <planet1> "" => "Jupiter" </planet1>
    <planet2> "" => "Jupiter" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Jupiter", "Saturn") => .K </k>
    <planet1> "" => "Jupiter" </planet1>
    <planet2> "" => "Saturn" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Jupiter", "Uranus") => .K </k>
    <planet1> "" => "Jupiter" </planet1>
    <planet2> "" => "Uranus" </planet2>
    <result> noResult => tupleValue("Saturn") </result>

  claim
    <k> verifyBF("Jupiter", "Neptune") => .K </k>
    <planet1> "" => "Jupiter" </planet1>
    <planet2> "" => "Neptune" </planet2>
    <result> noResult => tupleValue("Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Saturn", "Mercury") => .K </k>
    <planet1> "" => "Saturn" </planet1>
    <planet2> "" => "Mercury" </planet2>
    <result> noResult => tupleValue("Venus", "Earth", "Mars", "Jupiter") </result>

  claim
    <k> verifyBF("Saturn", "Venus") => .K </k>
    <planet1> "" => "Saturn" </planet1>
    <planet2> "" => "Venus" </planet2>
    <result> noResult => tupleValue("Earth", "Mars", "Jupiter") </result>

  claim
    <k> verifyBF("Saturn", "Earth") => .K </k>
    <planet1> "" => "Saturn" </planet1>
    <planet2> "" => "Earth" </planet2>
    <result> noResult => tupleValue("Mars", "Jupiter") </result>

  claim
    <k> verifyBF("Saturn", "Mars") => .K </k>
    <planet1> "" => "Saturn" </planet1>
    <planet2> "" => "Mars" </planet2>
    <result> noResult => tupleValue("Jupiter") </result>

  claim
    <k> verifyBF("Saturn", "Jupiter") => .K </k>
    <planet1> "" => "Saturn" </planet1>
    <planet2> "" => "Jupiter" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Saturn", "Saturn") => .K </k>
    <planet1> "" => "Saturn" </planet1>
    <planet2> "" => "Saturn" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Saturn", "Uranus") => .K </k>
    <planet1> "" => "Saturn" </planet1>
    <planet2> "" => "Uranus" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Saturn", "Neptune") => .K </k>
    <planet1> "" => "Saturn" </planet1>
    <planet2> "" => "Neptune" </planet2>
    <result> noResult => tupleValue("Uranus") </result>

  claim
    <k> verifyBF("Uranus", "Mercury") => .K </k>
    <planet1> "" => "Uranus" </planet1>
    <planet2> "" => "Mercury" </planet2>
    <result> noResult => tupleValue("Venus", "Earth", "Mars", "Jupiter", "Saturn") </result>

  claim
    <k> verifyBF("Uranus", "Venus") => .K </k>
    <planet1> "" => "Uranus" </planet1>
    <planet2> "" => "Venus" </planet2>
    <result> noResult => tupleValue("Earth", "Mars", "Jupiter", "Saturn") </result>

  claim
    <k> verifyBF("Uranus", "Earth") => .K </k>
    <planet1> "" => "Uranus" </planet1>
    <planet2> "" => "Earth" </planet2>
    <result> noResult => tupleValue("Mars", "Jupiter", "Saturn") </result>

  claim
    <k> verifyBF("Uranus", "Mars") => .K </k>
    <planet1> "" => "Uranus" </planet1>
    <planet2> "" => "Mars" </planet2>
    <result> noResult => tupleValue("Jupiter", "Saturn") </result>

  claim
    <k> verifyBF("Uranus", "Jupiter") => .K </k>
    <planet1> "" => "Uranus" </planet1>
    <planet2> "" => "Jupiter" </planet2>
    <result> noResult => tupleValue("Saturn") </result>

  claim
    <k> verifyBF("Uranus", "Saturn") => .K </k>
    <planet1> "" => "Uranus" </planet1>
    <planet2> "" => "Saturn" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Uranus", "Uranus") => .K </k>
    <planet1> "" => "Uranus" </planet1>
    <planet2> "" => "Uranus" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Uranus", "Neptune") => .K </k>
    <planet1> "" => "Uranus" </planet1>
    <planet2> "" => "Neptune" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Neptune", "Mercury") => .K </k>
    <planet1> "" => "Neptune" </planet1>
    <planet2> "" => "Mercury" </planet2>
    <result> noResult => tupleValue("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Neptune", "Venus") => .K </k>
    <planet1> "" => "Neptune" </planet1>
    <planet2> "" => "Venus" </planet2>
    <result> noResult => tupleValue("Earth", "Mars", "Jupiter", "Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Neptune", "Earth") => .K </k>
    <planet1> "" => "Neptune" </planet1>
    <planet2> "" => "Earth" </planet2>
    <result> noResult => tupleValue("Mars", "Jupiter", "Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Neptune", "Mars") => .K </k>
    <planet1> "" => "Neptune" </planet1>
    <planet2> "" => "Mars" </planet2>
    <result> noResult => tupleValue("Jupiter", "Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Neptune", "Jupiter") => .K </k>
    <planet1> "" => "Neptune" </planet1>
    <planet2> "" => "Jupiter" </planet2>
    <result> noResult => tupleValue("Saturn", "Uranus") </result>

  claim
    <k> verifyBF("Neptune", "Saturn") => .K </k>
    <planet1> "" => "Neptune" </planet1>
    <planet2> "" => "Saturn" </planet2>
    <result> noResult => tupleValue("Uranus") </result>

  claim
    <k> verifyBF("Neptune", "Uranus") => .K </k>
    <planet1> "" => "Neptune" </planet1>
    <planet2> "" => "Uranus" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF("Neptune", "Neptune") => .K </k>
    <planet1> "" => "Neptune" </planet1>
    <planet2> "" => "Neptune" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>

  claim
    <k> verifyBF(P1, P2) => .K </k>
    <planet1> "" => P1 </planet1>
    <planet2> "" => P2 </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
    requires P1 =/=String "Mercury" andBool P1 =/=String "Venus" andBool P1 =/=String "Earth" andBool P1 =/=String "Mars" andBool P1 =/=String "Jupiter" andBool P1 =/=String "Saturn" andBool P1 =/=String "Uranus" andBool P1 =/=String "Neptune"

  claim
    <k> verifyBF("Mercury", P2) => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => P2 </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
    requires P2 =/=String "Mercury" andBool P2 =/=String "Venus" andBool P2 =/=String "Earth" andBool P2 =/=String "Mars" andBool P2 =/=String "Jupiter" andBool P2 =/=String "Saturn" andBool P2 =/=String "Uranus" andBool P2 =/=String "Neptune"

  claim
    <k> verifyBF("Venus", P2) => .K </k>
    <planet1> "" => "Venus" </planet1>
    <planet2> "" => P2 </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
    requires P2 =/=String "Mercury" andBool P2 =/=String "Venus" andBool P2 =/=String "Earth" andBool P2 =/=String "Mars" andBool P2 =/=String "Jupiter" andBool P2 =/=String "Saturn" andBool P2 =/=String "Uranus" andBool P2 =/=String "Neptune"

  claim
    <k> verifyBF("Earth", P2) => .K </k>
    <planet1> "" => "Earth" </planet1>
    <planet2> "" => P2 </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
    requires P2 =/=String "Mercury" andBool P2 =/=String "Venus" andBool P2 =/=String "Earth" andBool P2 =/=String "Mars" andBool P2 =/=String "Jupiter" andBool P2 =/=String "Saturn" andBool P2 =/=String "Uranus" andBool P2 =/=String "Neptune"

  claim
    <k> verifyBF("Mars", P2) => .K </k>
    <planet1> "" => "Mars" </planet1>
    <planet2> "" => P2 </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
    requires P2 =/=String "Mercury" andBool P2 =/=String "Venus" andBool P2 =/=String "Earth" andBool P2 =/=String "Mars" andBool P2 =/=String "Jupiter" andBool P2 =/=String "Saturn" andBool P2 =/=String "Uranus" andBool P2 =/=String "Neptune"

  claim
    <k> verifyBF("Jupiter", P2) => .K </k>
    <planet1> "" => "Jupiter" </planet1>
    <planet2> "" => P2 </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
    requires P2 =/=String "Mercury" andBool P2 =/=String "Venus" andBool P2 =/=String "Earth" andBool P2 =/=String "Mars" andBool P2 =/=String "Jupiter" andBool P2 =/=String "Saturn" andBool P2 =/=String "Uranus" andBool P2 =/=String "Neptune"

  claim
    <k> verifyBF("Saturn", P2) => .K </k>
    <planet1> "" => "Saturn" </planet1>
    <planet2> "" => P2 </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
    requires P2 =/=String "Mercury" andBool P2 =/=String "Venus" andBool P2 =/=String "Earth" andBool P2 =/=String "Mars" andBool P2 =/=String "Jupiter" andBool P2 =/=String "Saturn" andBool P2 =/=String "Uranus" andBool P2 =/=String "Neptune"

  claim
    <k> verifyBF("Uranus", P2) => .K </k>
    <planet1> "" => "Uranus" </planet1>
    <planet2> "" => P2 </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
    requires P2 =/=String "Mercury" andBool P2 =/=String "Venus" andBool P2 =/=String "Earth" andBool P2 =/=String "Mars" andBool P2 =/=String "Jupiter" andBool P2 =/=String "Saturn" andBool P2 =/=String "Uranus" andBool P2 =/=String "Neptune"

  claim
    <k> verifyBF("Neptune", P2) => .K </k>
    <planet1> "" => "Neptune" </planet1>
    <planet2> "" => P2 </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
    requires P2 =/=String "Mercury" andBool P2 =/=String "Venus" andBool P2 =/=String "Earth" andBool P2 =/=String "Mars" andBool P2 =/=String "Jupiter" andBool P2 =/=String "Saturn" andBool P2 =/=String "Uranus" andBool P2 =/=String "Neptune"
endmodule
