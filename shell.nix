let pkgs = import (builtins.fetchTarball {
      url = "https://github.com/NixOS/nixpkgs/archive/66acfa3d16eb599f5aa85bda153a24742f683383.tar.gz";
    }) {
      config.allowUnfree = true;
    };

    customizedPython = pkgs.python3.withPackages (python-packages: with python-packages;
      let computation = [
            numpy pandas
          ];
          ide = [ jupyterlab ipywidgets ipydatawidgets ];
          viz = [ matplotlib tqdm graphviz];
      in computation ++ ide ++ viz);

in pkgs.mkShell rec {
  name = "alphaflow";
  buildInputs = with pkgs; [ customizedPython ];
}
