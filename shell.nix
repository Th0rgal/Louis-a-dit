with import <nixpkgs> { };

let
  louis = python38.withPackages (python-packages:
    with python-packages; [
      discordpy
      pillow
      toml
    ]);
in stdenv.mkDerivation {
  name = "louis-dev-environment";
  buildInputs = [ louis ];
}
