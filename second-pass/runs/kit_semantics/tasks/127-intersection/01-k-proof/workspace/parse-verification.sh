#!/bin/sh
exec kast --definition verification-kompiled --module VERIFICATION --output kore "$@"
