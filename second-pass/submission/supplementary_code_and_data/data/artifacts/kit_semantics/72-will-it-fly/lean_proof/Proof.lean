import Klean72WillItFly.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-ec583fc3f12bafee23d7f302c742e52ce776b44b86fb0ae71114dc6dcdb3bb9f, rule-3905ebe2499ea5ede82420688c2f2bdadaaf27ab8b44aef52876a9281ba13c4e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool := left && right

private def valAsK (value : SortVal) : SortK :=
  SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk

-- The frozen Int/Bool conversion rules have no non-integral case. This branch
-- only completes the generated total Lean type; every obligation using it is
-- guarded by integralV.
private def intValue (value : SortVal) : SortInt :=
  match value with
  | SortVal.inj_SortInt number => number
  | SortVal.inj_SortBool flag => if flag then 1 else 0
  | _ => 0

private def projectBool?Impl : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortBool value) SortK.dotk => some value
  | _ => none

private def projectFloat?Impl : SortK → Option SortFloat
  | SortK.kseq (SortKItem.inj_SortFloat value) SortK.dotk => some value
  | _ => none

private def projectInt?Impl : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => some value
  | _ => none

-- These classifiers are exactly the definedness observations of the three
-- K sort projections on singleton computations.
private def isBoolImpl (term : SortK) : SortBool :=
  (projectBool?Impl term).isSome

private def isFloatImpl (term : SortK) : SortBool :=
  (projectFloat?Impl term).isSome

private def isIntImpl (term : SortK) : SortBool :=
  (projectInt?Impl term).isSome

/- KORE symbol: LblfloatV'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Val; frozen source obligations: rule-aea328b93abee3d0539e019d0745462924337ff6c0e980f560da1a6fa1c0b72e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «floatV(_)_VERIFICATION-SYNTAX_Bool_Val» (value : SortVal) : SortBool :=
  let term := valAsK value
  (isFloatImpl term && !isIntImpl term) && !isBoolImpl term
/- KORE symbol: LblintLikeTotal; frozen source obligations: rule-82314b210da1b2e71ed9cacdc03ed14b6f144d73a7db17b8f0b5688eb4d30e92. Replace this stub with its honest total meaning from the frozen K semantics. -/
def intLikeTotal (value : SortVal) : SortInt := intValue value
/- KORE symbol: LblintOf'LParUndsRParUnds'MPY-BUILTINS'Unds'Int'Unds'Val; frozen source obligations: rule-82314b210da1b2e71ed9cacdc03ed14b6f144d73a7db17b8f0b5688eb4d30e92. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «intOf(_)_MPY-BUILTINS_Int_Val» (value : SortVal) : SortInt :=
  match value with
  | SortVal.inj_SortInt number => number
  | SortVal.inj_SortBool flag => if flag then 1 else 0
  | _ => 1
/- KORE symbol: LblintegralV'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Val; frozen source obligations: rule-82314b210da1b2e71ed9cacdc03ed14b6f144d73a7db17b8f0b5688eb4d30e92. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «integralV(_)_VERIFICATION-SYNTAX_Bool_Val» (value : SortVal) : SortBool :=
  let term := valAsK value
  ((isIntImpl term && !isBoolImpl term) ||
      (isBoolImpl term && !isIntImpl term)) &&
    !isFloatImpl term
/- KORE symbol: LblisBool; frozen source obligations: rule-ec583fc3f12bafee23d7f302c742e52ce776b44b86fb0ae71114dc6dcdb3bb9f, rule-3905ebe2499ea5ede82420688c2f2bdadaaf27ab8b44aef52876a9281ba13c4e, rule-223d04d630bd21ce9624149f41397f24c0af78120813951d1f3ef073273e8a83. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isBool (term : SortK) : SortBool := isBoolImpl term
/- KORE symbol: LblisFloat; frozen source obligations: rule-ec583fc3f12bafee23d7f302c742e52ce776b44b86fb0ae71114dc6dcdb3bb9f, rule-3905ebe2499ea5ede82420688c2f2bdadaaf27ab8b44aef52876a9281ba13c4e, rule-725c0275ed9c194a24cc6686a7d8ac0e05163edac4687c027a68f98431430868. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isFloat (term : SortK) : SortBool := isFloatImpl term
/- KORE symbol: LblisInt; frozen source obligations: rule-ec583fc3f12bafee23d7f302c742e52ce776b44b86fb0ae71114dc6dcdb3bb9f, rule-90eb7f013a9e927996889600de0ac06a1c48fe1f32ff329772fa38b5022a8a28, rule-3905ebe2499ea5ede82420688c2f2bdadaaf27ab8b44aef52876a9281ba13c4e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt (term : SortK) : SortBool := isIntImpl term
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-ec583fc3f12bafee23d7f302c742e52ce776b44b86fb0ae71114dc6dcdb3bb9f, rule-3905ebe2499ea5ede82420688c2f2bdadaaf27ab8b44aef52876a9281ba13c4e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool := !value
/- KORE symbol: Lblproject'Coln'Bool; frozen source obligations: rule-3905ebe2499ea5ede82420688c2f2bdadaaf27ab8b44aef52876a9281ba13c4e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Bool» (term : SortK) : SortBool :=
  (projectBool?Impl term).getD false
/- KORE symbol: Lblproject'Coln'Float; frozen source obligations: rule-aea328b93abee3d0539e019d0745462924337ff6c0e980f560da1a6fa1c0b72e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Float» (term : SortK) : SortFloat :=
  (projectFloat?Impl term).getD default
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-ec583fc3f12bafee23d7f302c742e52ce776b44b86fb0ae71114dc6dcdb3bb9f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» (term : SortK) : SortInt :=
  (projectInt?Impl term).getD 0
/- KORE symbol: LblprojectBoolTotal; frozen source obligations: rule-3905ebe2499ea5ede82420688c2f2bdadaaf27ab8b44aef52876a9281ba13c4e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectBoolTotal (value : SortVal) : SortBool :=
  match value with
  | SortVal.inj_SortBool flag => flag
  | _ => true
/- KORE symbol: LblprojectFloatTotal; frozen source obligations: rule-aea328b93abee3d0539e019d0745462924337ff6c0e980f560da1a6fa1c0b72e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectFloatTotal (value : SortVal) : SortFloat :=
  match value with
  | SortVal.inj_SortFloat number => number
  | _ => 1.0
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-ec583fc3f12bafee23d7f302c742e52ce776b44b86fb0ae71114dc6dcdb3bb9f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal (value : SortVal) : SortInt :=
  match value with
  | SortVal.inj_SortInt number => number
  | _ => 1
/- KORE symbol: Lblproject'Coln'Bool; frozen source obligations: rule-223d04d630bd21ce9624149f41397f24c0af78120813951d1f3ef073273e8a83. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Bool?» (term : SortK) : Option SortBool :=
  projectBool?Impl term
/- KORE symbol: Lblproject'Coln'Float; frozen source obligations: rule-725c0275ed9c194a24cc6686a7d8ac0e05163edac4687c027a68f98431430868. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Float?» (term : SortK) : Option SortFloat :=
  projectFloat?Impl term
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-90eb7f013a9e927996889600de0ac06a1c48fe1f32ff329772fa38b5022a8a28. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» (term : SortK) : Option SortInt :=
  projectInt?Impl term

theorem final :
    Klean72WillItFly.Lemmas.targetStatement _andBool_ «floatV(_)_VERIFICATION-SYNTAX_Bool_Val» intLikeTotal «intOf(_)_MPY-BUILTINS_Int_Val» «integralV(_)_VERIFICATION-SYNTAX_Bool_Val» isBool isFloat isInt notBool_ «project:Bool» «project:Float» «project:Int» projectBoolTotal projectFloatTotal projectIntTotal «project:Bool?» «project:Float?» «project:Int?» := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro V h
    cases V <;>
      simp_all [_andBool_, notBool_, isInt, isBool, isFloat,
        isIntImpl, isBoolImpl, isFloatImpl, projectIntTotal,
        «project:Int», projectInt?Impl, projectBool?Impl,
        projectFloat?Impl, inj]
  · intro V
    simp [isInt, isIntImpl, «project:Int?»]
  · intro V h
    cases V <;>
      simp_all [_andBool_, notBool_, isInt, isBool, isFloat,
        isIntImpl, isBoolImpl, isFloatImpl, projectBoolTotal,
        «project:Bool», projectInt?Impl, projectBool?Impl,
        projectFloat?Impl, inj]
  · intro V
    simp [isBool, isBoolImpl, «project:Bool?»]
  · intro V h
    cases V <;>
      simp_all [«floatV(_)_VERIFICATION-SYNTAX_Bool_Val»,
        isIntImpl, isBoolImpl, isFloatImpl, projectFloatTotal,
        «project:Float», projectInt?Impl, projectBool?Impl,
        projectFloat?Impl, valAsK, inj]
  · intro V
    simp [isFloat, isFloatImpl, «project:Float?»]
  · intro V h
    cases V <;>
      simp_all [«integralV(_)_VERIFICATION-SYNTAX_Bool_Val»,
        intLikeTotal, intValue, «intOf(_)_MPY-BUILTINS_Int_Val»,
        isIntImpl, isBoolImpl, isFloatImpl, projectInt?Impl,
        projectBool?Impl, projectFloat?Impl, valAsK, inj]

end Proof
