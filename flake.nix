{
  description = "Colour-science project";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs =
    { nixpkgs, ... }:
    {
      devShells.x86_64-linux =
        let
          pkgs = nixpkgs.legacyPackages.x86_64-linux;
        in
        {
          default = (pkgs.mkShell.override {stdenv = pkgs.gccStdenv;}) {
            packages = [ 
              pkgs.gtk2
              (pkgs.python311.withPackages (ps: [
                ps.numpy
                ps.pandas
                ps.matplotlib
                (ps.callPackage ./colour-science.nix {})
              ])
            )];
            buildInputs = with pkgs; [
              qt5.qtwayland
              libsForQt5.qt5.wrapQtAppsHook
            ];
            LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
              pkgs.gtk2
            ];
            QT_PLUGIN_PATH = with pkgs.qt5; "${qtbase}/${qtbase.qtPluginPrefix}";
          };
        };
    };
}
