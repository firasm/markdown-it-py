from markdown_it import MarkdownIt
from markdown_it.utils import AttrDict


def test_ref_definitions():

    md = MarkdownIt()
    src = "[a]: abc\n\n[b]: xyz\n\n[b]: ijk"
    env = AttrDict()
    tokens = md.parse(src, env)
    assert tokens == []
    assert env == {
        "references": {
            "A": {"title": "", "href": "abc", "map": [0, 1]},
            "B": {"title": "", "href": "xyz", "map": [2, 3]},
        },
        "duplicate_refs": [{"href": "ijk", "label": "B", "map": [4, 5], "title": ""}],
    }


def test_use_existing_env(data_regression):
    md = MarkdownIt()
    src = "[a]\n\n[c]: ijk"
    env = AttrDict(
        {
            "references": {
                "A": {"title": "", "href": "abc", "map": [0, 1]},
                "B": {"title": "", "href": "xyz", "map": [2, 3]},
            }
        }
    )
    tokens = md.parse(src, env)
    data_regression.check([token.as_dict() for token in tokens])
    assert env == {
        "references": {
            "A": {"title": "", "href": "abc", "map": [0, 1]},
            "B": {"title": "", "href": "xyz", "map": [2, 3]},
            "C": {"title": "", "href": "ijk", "map": [2, 3]},
        }
    }


def test_store_labels(data_regression):
    md = MarkdownIt()
    md.options["store_labels"] = True
    src = "[a]\n\n![a]\n\n[a]: ijk"
    tokens = md.parse(src)
    data_regression.check([token.as_dict() for token in tokens])
