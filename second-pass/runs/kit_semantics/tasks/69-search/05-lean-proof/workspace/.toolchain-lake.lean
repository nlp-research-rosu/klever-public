import Lake
import Lean.Elab.Frontend
import Lean.Compiler.IR.EmitC

open Lake DSL
open System

package toolchain_bridge

private structure CompileArgs where
  source : Option FilePath := none
  olean : Option FilePath := none
  ilean : Option FilePath := none
  cFile : Option FilePath := none
  setup : Option FilePath := none

private def parseCompileArgs (args : List String) : Except String CompileArgs := do
  let rec go (args : List String) (result : CompileArgs) : Except String CompileArgs := do
    match args with
    | [] => pure result
    | "-o" :: path :: rest => go rest { result with olean := some path }
    | "-i" :: path :: rest => go rest { result with ilean := some path }
    | "-c" :: path :: rest => go rest { result with cFile := some path }
    | "--setup" :: path :: rest => go rest { result with setup := some path }
    | "-D" :: _ :: rest => go rest result
    | "-s" :: _ :: rest => go rest result
    | "--json" :: rest => go rest result
    | arg :: rest =>
      if arg.endsWith ".lean" then
        go rest { result with source := some arg }
      else
        go rest result
  go args {}

script compile args do
  let parsed ← IO.ofExcept <| parseCompileArgs args
  let source ←
    match parsed.source with
    | some source => pure source
    | none => throw <| IO.userError "missing Lean source"
  let setupFile ←
    match parsed.setup with
    | some setup => pure setup
    | none => throw <| IO.userError "missing module setup"
  let setup ← Lean.ModuleSetup.load setupFile
  let input ← IO.FS.readFile source
  let opts : Lean.Options :=
    ({} : Lean.Options)
      |>.setNat `maxHeartbeats 10000000
      |>.setNat `maxRecDepth 100000
  let env? ← Lean.Elab.runFrontend
    input opts source.toString setup.name 0 parsed.olean parsed.ilean
    false #[] #[] false (some setup)
  let env ←
    match env? with
    | some env => pure env
    | none => throw <| IO.userError s!"elaboration failed: {source}"
  if let some cFile := parsed.cFile then
    IO.FS.writeFile cFile <| ← IO.ofExcept <| Lean.IR.emitC env setup.name
  return 0
