"""A corpus composed from ordered locations honors feature precedence.

A later location overrides features of an earlier one in every load mode,
including after compiling the composition, and a compiled cache left behind
by loading the base location alone never stands in for the composition.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import LOAD_MODES, open_corpus

SECTIONS = ("@sectionFeatures=sentence_id,phrase_id", "@sectionTypes=sentence,phrase")


def _override_module(base: Path, tmp_path: Path) -> Path:
    module = tmp_path / "override"
    module.mkdir()
    word = (base / "word.tf").read_text(encoding="utf-8")
    (module / "word.tf").write_text(word.replace("hello", "OVERRIDDEN"), encoding="utf-8")
    return module


@pytest.mark.parametrize("mode", LOAD_MODES)
def test_later_location_overrides_earlier(mini_corpus_with_otext, tmp_path, mode):
    base = mini_corpus_with_otext(*SECTIONS)
    override = _override_module(base, tmp_path)

    # Leave behind whatever cache loading the base location alone produces.
    assert open_corpus([base], "loadAll", tmp_path).F.word.v(1) == "hello"

    api = open_corpus([base, override], mode, tmp_path)
    assert api.F.word.v(1) == "OVERRIDDEN"
    assert api.T.nodeFromSection(("S1", 1)) == 6


@pytest.mark.parametrize("mode", LOAD_MODES)
def test_multiple_locations_preserve_modules(mini_corpus_with_otext, tmp_path, mode):
    from cfabric import Fabric

    base = mini_corpus_with_otext(*SECTIONS)
    override = _override_module(base, tmp_path)
    base_root, extra_root = tmp_path / "base", tmp_path / "extra"
    base_root.mkdir()
    extra_root.mkdir()
    base.rename(base_root / "tf")
    override.rename(extra_root / "tf")
    fabric = Fabric(locations=[str(base_root), str(extra_root)], modules=["tf"], silent="deep")
    if mode == "openMapped":
        cache = tmp_path / "modules.cfr"
        assert fabric.compile(str(cache), None, "deep")
        api = fabric.openMapped(str(cache))
    elif mode == "load":
        api = fabric.load("word", silent="deep")
    else:
        api = fabric.loadAll(silent="deep")
    assert api.F.word.v(1) == "OVERRIDDEN"
    assert api.T.nodeFromSection(("S1", 1)) == 6
