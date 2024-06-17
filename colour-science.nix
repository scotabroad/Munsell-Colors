# colour-science.nix
{ lib
, buildPythonPackage
, fetchPypi
, setuptools
, wheel
# dependencies
, imageio
, numpy
, scipy
, typing-extensions
#below is optional
, graphviz
, matplotlib
, networkx
, pandas
, pygraphviz
, tqdm
, trimesh
, xxhash
#, biblib-simple #missing
, coverage
, coveralls
, invoke
, jupyter
, poetry-core
, pydata-sphinx-theme
, pytest
, pytest-cov
, pytest-xdist
, restructuredtext-lint
, sphinx
, sphinxcontrib-bibtex
, toml
, twine
, opencolorio #optional non-python runtime
, openimageio #optional non-python runtime
, pre-commit #build time
, pyright #build time
}:

buildPythonPackage rec {
  pname = "colour_science";
  version = "0.4.4";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-o8s7jopR24K2JSQXPWWucDlr+pQ2NuER5Q+3zBJYV60=";
  };

  # do not run tests
  doCheck = false;

  pyproject = true;

  # specific to buildPythonPackage, see its reference
  dependencies = [ #run-time python dependencies
    imageio
    numpy
    scipy
    typing-extensions
    #below is optional
    graphviz
    matplotlib
    networkx
    pandas
    pygraphviz
    tqdm
    trimesh
    xxhash
  ];
  build-system = [ #build time python dependencies
    #biblib-simple #missing
    coverage
    coveralls
    invoke
    jupyter
    poetry-core
    pydata-sphinx-theme
    pytest
    pytest-cov
    pytest-xdist
    restructuredtext-lint
    sphinx
    sphinxcontrib-bibtex
    toml
    twine
  ];
  build-inputs = [ #build and/or runtime non-python libraries
    opencolorio #optional non-python runtime
    openimageio #optional non-python runtime
    pre-commit #build time
    pyright #build time
  ];
}
