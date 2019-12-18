import logging

from typing import Text, List, Optional, Dict, Any

from rasa.nlu.components import Component
from rasa.nlu.constants import RESPONSE_ATTRIBUTE, TEXT_ATTRIBUTE, CLS_TOKEN

logger = logging.getLogger(__name__)


class Token(object):
    def __init__(
        self,
        text: Text,
        start: int,
        data: Optional[Dict[Text, Any]] = None,
        lemma: Optional[Text] = None,
        end: Optional[int] = None,
    ) -> None:
        self.start = start
        self.text = text
        self.end = start + len(text)
        self.data = data if data else {}
        self.lemma = lemma or text
        self.end = end if end else start + len(text)

    def set(self, prop: Text, info: Any) -> None:
        self.data[prop] = info

    def get(self, prop: Text, default: Optional[Any] = None) -> Any:
        return self.data.get(prop, default)

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (self.start, self.end, self.text, self.lemma) == (
            other.start,
            other.end,
            other.text,
            other.lemma,
        )

    def __lt__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (self.start, self.end, self.text, self.lemma) < (
            other.start,
            other.end,
            other.text,
            other.lemma,
        )


class Tokenizer(Component):
    def add_cls_token(
        self, tokens: List[Token], attribute: Text = TEXT_ATTRIBUTE
    ) -> List[Token]:
        if attribute in [RESPONSE_ATTRIBUTE, TEXT_ATTRIBUTE] and tokens:
            # +1 to have a space between the last token and the __cls__ token
            idx = tokens[-1].end + 1
            tokens.append(Token(CLS_TOKEN, idx))

        return tokens
