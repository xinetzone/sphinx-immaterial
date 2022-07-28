from typing import Type, Tuple

import docutils.nodes
import sphinx.addnodes
import sphinx.domains.python


def _monkey_patch_pyattribute_handle_signature(
    directive_cls: Type[sphinx.domains.python.PyObject],
):
    """Modifies PyAttribute or PyVariable to improve styling of signature."""

    def handle_signature(
        self, sig: str, signode: sphinx.addnodes.desc_signature
    ) -> Tuple[str, str]:
        result = super(directive_cls, self).handle_signature(sig, signode)
        typ = self.options.get("type")
        if typ:
            signode += sphinx.addnodes.desc_sig_punctuation("", " : ")
            signode += sphinx.domains.python._parse_annotation(typ, self.env)

        value = self.options.get("value")
        if value:
            signode += sphinx.addnodes.desc_sig_punctuation("", " = ")
            signode += docutils.nodes.literal(
                text=value, classes=["code", "python"], language="python"
            )
        return result

    directive_cls.handle_signature = handle_signature  # type: ignore


_monkey_patch_pyattribute_handle_signature(sphinx.domains.python.PyAttribute)
_monkey_patch_pyattribute_handle_signature(sphinx.domains.python.PyVariable)
