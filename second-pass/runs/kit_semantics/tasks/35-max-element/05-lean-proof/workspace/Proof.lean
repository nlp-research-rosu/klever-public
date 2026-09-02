import Proof.Operational

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-0dd31e82f28e4e2268dc5cc10687de07aaa748c918fc5655ad750edc7d27060e, rule-23d7b940397fb8e3365532e4a44710e62c2afe797886ebd6bdd7d8fe6e2f503d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ : SortBool → SortBool → SortBool := Operational.boolAndImpl
/- KORE symbol: Lbl'Unds'orBool'Unds'; frozen source obligations: rule-217c86e6ea02fd8a4d522673cccf435e5bd87a23e18f17f498dfd31b0197c5d2, rule-fd5dc7e25c9b6aa2d8b03dc179dba72357ad91d531372a1f977f6d6f5ddf44ba, rule-add4293d1db932d0d69adaa4f5856603221b0a4520153f408fd85c3d29640f08. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _orBool_ : SortBool → SortBool → SortBool := Operational.boolOrImpl
/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-15d2159bad2a7aea7a496c3fcc1a2424c1e94a787eca67f2288469b2dd32820e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» : SortInt → SortInt → SortBool := Operational.intGreaterImpl
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-15d2159bad2a7aea7a496c3fcc1a2424c1e94a787eca67f2288469b2dd32820e, rule-0dd31e82f28e4e2268dc5cc10687de07aaa748c918fc5655ad750edc7d27060e, rule-23d7b940397fb8e3365532e4a44710e62c2afe797886ebd6bdd7d8fe6e2f503d. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool := Operational.cmpDispatchImpl
/- KORE symbol: LblcodesOf'LParUndsRParUnds'VERIFICATION'Unds'IntSeq'Unds'Str; frozen source obligations: rule-23d7b940397fb8e3365532e4a44710e62c2afe797886ebd6bdd7d8fe6e2f503d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «codesOf(_)_VERIFICATION_IntSeq_Str» : SortStr → SortIntSeq := Operational.codesFromStrImpl
/- KORE symbol: LblisBool; frozen source obligations: rule-94291474df49f0025fadd1e009e9c1267cf9fc22cb9d891f2604783277c3365c, rule-da035816c11ad6dff67d5301ca6654c3f3a6aa6e611daf47d9809952ebb70c73, rule-217c86e6ea02fd8a4d522673cccf435e5bd87a23e18f17f498dfd31b0197c5d2, rule-fd5dc7e25c9b6aa2d8b03dc179dba72357ad91d531372a1f977f6d6f5ddf44ba, rule-add4293d1db932d0d69adaa4f5856603221b0a4520153f408fd85c3d29640f08. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isBool : SortK → SortBool := Operational.isBoolImpl
/- KORE symbol: LblisFloat; frozen source obligations: rule-97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e, rule-0efb958402771e00f0c87dc7fc8ee7185fb8aee4c9d4eb3d4fe5a2200a1a9fac, rule-217c86e6ea02fd8a4d522673cccf435e5bd87a23e18f17f498dfd31b0197c5d2, rule-fd5dc7e25c9b6aa2d8b03dc179dba72357ad91d531372a1f977f6d6f5ddf44ba, rule-add4293d1db932d0d69adaa4f5856603221b0a4520153f408fd85c3d29640f08. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isFloat : SortK → SortBool := Operational.isFloatImpl
/- KORE symbol: LblisInt; frozen source obligations: rule-83a120e7a0765b750dbc0ef3eb515f2d8b64c7b50538b3bebbd1cc4789cf8d3e, rule-0c81e675943b09f77b3c9bcde8bf866227b1fb965fcb1d308e097cea0abff848, rule-15d2159bad2a7aea7a496c3fcc1a2424c1e94a787eca67f2288469b2dd32820e, rule-217c86e6ea02fd8a4d522673cccf435e5bd87a23e18f17f498dfd31b0197c5d2, rule-fd5dc7e25c9b6aa2d8b03dc179dba72357ad91d531372a1f977f6d6f5ddf44ba, rule-add4293d1db932d0d69adaa4f5856603221b0a4520153f408fd85c3d29640f08. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool := Operational.isIntImpl
/- KORE symbol: LblisNumericV'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0dd31e82f28e4e2268dc5cc10687de07aaa748c918fc5655ad750edc7d27060e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isNumericV(_)_VERIFICATION_Bool_Val» : SortVal → SortBool := Operational.numericImpl
/- KORE symbol: LblisStr; frozen source obligations: rule-eba3d8bb8496c9c5885aaf564d4bb58cbf5f171260b498cb2ecf9199e4de2bb6, rule-3802c35df0656a078865fc6fd93f989eff8400fa623325e53283e267b01869a2, rule-23d7b940397fb8e3365532e4a44710e62c2afe797886ebd6bdd7d8fe6e2f503d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isStr : SortK → SortBool := Operational.isStrImpl
/- KORE symbol: LblmaxFOpaque; frozen source obligations: rule-d3c655f03d0599014d0675fb90b301045c507f274904692d149e1aa3aa5fcc6e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def maxFOpaque : SortFloat → SortFloat → SortFloat := Operational.floatMaxImpl
/- KORE symbol: LblmaxFloat'LParUndsCommUndsRParUnds'FLOAT'Unds'Float'Unds'Float'Unds'Float; frozen source obligations: rule-d3c655f03d0599014d0675fb90b301045c507f274904692d149e1aa3aa5fcc6e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «maxFloat(_,_)_FLOAT_Float_Float_Float» : SortFloat → SortFloat → SortFloat := Operational.floatMaxImpl
/- KORE symbol: LblnumericGt'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'NumericView'Unds'NumericView; frozen source obligations: rule-0dd31e82f28e4e2268dc5cc10687de07aaa748c918fc5655ad750edc7d27060e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «numericGt(_,_)_VERIFICATION_Bool_NumericView_NumericView» : SortNumericView → SortNumericView → SortBool := Operational.numericGreaterImpl
/- KORE symbol: LblnumericView'LParUndsRParUnds'VERIFICATION'Unds'NumericView'Unds'Val; frozen source obligations: rule-0dd31e82f28e4e2268dc5cc10687de07aaa748c918fc5655ad750edc7d27060e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «numericView(_)_VERIFICATION_NumericView_Val» : SortVal → SortNumericView := Operational.numericViewImpl
/- KORE symbol: Lblproject'Coln'Bool; frozen source obligations: rule-da035816c11ad6dff67d5301ca6654c3f3a6aa6e611daf47d9809952ebb70c73. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Bool» : SortK → SortBool := Operational.boolProjectionImpl
/- KORE symbol: Lblproject'Coln'Float; frozen source obligations: rule-0efb958402771e00f0c87dc7fc8ee7185fb8aee4c9d4eb3d4fe5a2200a1a9fac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Float» : SortK → SortFloat := Operational.floatProjectionImpl
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0c81e675943b09f77b3c9bcde8bf866227b1fb965fcb1d308e097cea0abff848. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» : SortK → SortInt := Operational.intProjectionImpl
/- KORE symbol: Lblproject'Coln'Str; frozen source obligations: rule-3802c35df0656a078865fc6fd93f989eff8400fa623325e53283e267b01869a2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Str» : SortK → SortStr := Operational.strProjectionImpl
/- KORE symbol: LblprojectBoolTotal; frozen source obligations: rule-da035816c11ad6dff67d5301ca6654c3f3a6aa6e611daf47d9809952ebb70c73. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectBoolTotal : SortVal → SortBool := Operational.boolTotalProjectionImpl
/- KORE symbol: LblprojectFloatTotal; frozen source obligations: rule-0efb958402771e00f0c87dc7fc8ee7185fb8aee4c9d4eb3d4fe5a2200a1a9fac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectFloatTotal : SortVal → SortFloat := Operational.floatTotalProjectionImpl
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-0c81e675943b09f77b3c9bcde8bf866227b1fb965fcb1d308e097cea0abff848, rule-15d2159bad2a7aea7a496c3fcc1a2424c1e94a787eca67f2288469b2dd32820e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal : SortVal → SortInt := Operational.intTotalProjectionImpl
/- KORE symbol: LblprojectStrTotal; frozen source obligations: rule-3802c35df0656a078865fc6fd93f989eff8400fa623325e53283e267b01869a2, rule-23d7b940397fb8e3365532e4a44710e62c2afe797886ebd6bdd7d8fe6e2f503d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectStrTotal : SortVal → SortStr := Operational.strTotalProjectionImpl
/- KORE symbol: LblstrLt'LParUndsCommUndsRParUnds'MPY-STR'Unds'Bool'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-23d7b940397fb8e3365532e4a44710e62c2afe797886ebd6bdd7d8fe6e2f503d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» : SortIntSeq → SortIntSeq → SortBool := Operational.strLessImpl
/- KORE symbol: Lblproject'Coln'Bool; frozen source obligations: rule-94291474df49f0025fadd1e009e9c1267cf9fc22cb9d891f2604783277c3365c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Bool?» : SortK → Option SortBool := Operational.boolProjectionOptImpl
/- KORE symbol: Lblproject'Coln'Float; frozen source obligations: rule-97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Float?» : SortK → Option SortFloat := Operational.floatProjectionOptImpl
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-83a120e7a0765b750dbc0ef3eb515f2d8b64c7b50538b3bebbd1cc4789cf8d3e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt := Operational.intProjectionOptImpl
/- KORE symbol: Lblproject'Coln'Str; frozen source obligations: rule-eba3d8bb8496c9c5885aaf564d4bb58cbf5f171260b498cb2ecf9199e4de2bb6. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Str?» : SortK → Option SortStr := Operational.strProjectionOptImpl

theorem final :
    Klean35MaxElement.Lemmas.targetStatement _andBool_ _orBool_ «_>Int_» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «codesOf(_)_VERIFICATION_IntSeq_Str» isBool isFloat isInt «isNumericV(_)_VERIFICATION_Bool_Val» isStr maxFOpaque «maxFloat(_,_)_FLOAT_Float_Float_Float» «numericGt(_,_)_VERIFICATION_Bool_NumericView_NumericView» «numericView(_)_VERIFICATION_NumericView_Val» «project:Bool» «project:Float» «project:Int» «project:Str» projectBoolTotal projectFloatTotal projectIntTotal projectStrTotal «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» «project:Bool?» «project:Float?» «project:Int?» «project:Str?» := by
  unfold Klean35MaxElement.Lemmas.targetStatement
  constructor
  · intro v
    simp [«project:Int?», isInt, Operational.isIntImpl]
  constructor
  · intro v h
    cases v <;>
      simp [Operational.injValItem_eq, «project:Int», projectIntTotal,
        Operational.intProjectionImpl, Operational.intProjectionOptImpl,
        Operational.intTotalProjectionImpl, Operational.valItemImpl] at h ⊢
  constructor
  · intro m v h
    cases v <;>
      simp [Operational.injValItem_eq, isInt, Operational.isIntImpl,
        Operational.intProjectionOptImpl,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val», Operational.cmpDispatchImpl,
        «_>Int_», projectIntTotal, Operational.intTotalProjectionImpl,
        Operational.intCompareImpl, Operational.intGreaterImpl,
        Operational.valItemImpl] at h ⊢
  constructor
  · intro v
    simp [«project:Float?», isFloat, Operational.isFloatImpl]
  constructor
  · intro v h
    cases v <;>
      simp [Operational.injValItem_eq, «project:Float», projectFloatTotal,
        Operational.floatProjectionImpl, Operational.floatProjectionOptImpl,
        Operational.floatTotalProjectionImpl, Operational.valItemImpl] at h ⊢
  constructor
  · intro f₂ f₁
    rfl
  constructor
  · intro v
    simp [«project:Bool?», isBool, Operational.isBoolImpl]
  constructor
  · intro v h
    cases v <;>
      simp [Operational.injValItem_eq, «project:Bool», projectBoolTotal,
        Operational.boolProjectionImpl, Operational.boolProjectionOptImpl,
        Operational.boolTotalProjectionImpl, Operational.valItemImpl] at h ⊢
  constructor
  · intro v
    simp [«project:Str?», isStr, Operational.isStrImpl]
  constructor
  · intro v h
    cases v <;>
      simp [Operational.injValItem_eq, «project:Str», projectStrTotal,
        Operational.strProjectionImpl, Operational.strProjectionOptImpl,
        Operational.strTotalProjectionImpl, Operational.valItemImpl] at h ⊢
  constructor
  · intro m v h
    cases v <;> cases m <;>
      simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        Operational.cmpDispatchImpl, _andBool_, Operational.boolAndImpl,
        «isNumericV(_)_VERIFICATION_Bool_Val», Operational.numericImpl,
        «numericGt(_,_)_VERIFICATION_Bool_NumericView_NumericView»,
        Operational.numericGreaterImpl,
        «numericView(_)_VERIFICATION_NumericView_Val»,
        Operational.numericViewImpl, Operational.intCompareImpl,
        Operational.floatCompareImpl, Operational.intFloatCompareImpl,
        Operational.floatIntCompareImpl, Operational.intGreaterImpl] at h ⊢
  constructor
  · intro m v h
    cases v <;> cases m <;>
      simp [Operational.injValItem_eq, _andBool_, Operational.boolAndImpl,
        isStr, Operational.isStrImpl, Operational.strProjectionOptImpl,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        Operational.cmpDispatchImpl, Operational.strCompareImpl,
        «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq»,
        «codesOf(_)_VERIFICATION_IntSeq_Str», projectStrTotal,
        Operational.strTotalProjectionImpl, Operational.valItemImpl] at h ⊢
  constructor
  · intro v h
    cases v <;>
      simp [Operational.injValItem_eq, isInt, isFloat, isBool,
        Operational.isIntImpl, Operational.isFloatImpl, Operational.isBoolImpl,
        Operational.intProjectionOptImpl, Operational.floatProjectionOptImpl,
        Operational.boolProjectionOptImpl, _orBool_, Operational.boolOrImpl,
        Operational.valItemImpl] at h ⊢
  constructor
  · intro v h
    cases v <;>
      simp [Operational.injValItem_eq, isInt, isFloat, isBool,
        Operational.isIntImpl, Operational.isFloatImpl, Operational.isBoolImpl,
        Operational.intProjectionOptImpl, Operational.floatProjectionOptImpl,
        Operational.boolProjectionOptImpl, _orBool_, Operational.boolOrImpl,
        Operational.valItemImpl] at h ⊢
  · intro v h
    cases v <;>
      simp [Operational.injValItem_eq, isInt, isFloat, isBool,
        Operational.isIntImpl, Operational.isFloatImpl, Operational.isBoolImpl,
        Operational.intProjectionOptImpl, Operational.floatProjectionOptImpl,
        Operational.boolProjectionOptImpl, _orBool_, Operational.boolOrImpl,
        Operational.valItemImpl] at h ⊢

end Proof
