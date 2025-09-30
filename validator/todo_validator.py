from typing import Annotated, Optional
from pydantic import BeforeValidator, StringConstraints


def _trim(v):
    return v.strip() if isinstance(v, str) else v


def _none_if_empty(v):
    if isinstance(v, str):
        s = v.strip()
        return s if s else None
    return v


TitleRule = Annotated[
    str,
    BeforeValidator(_trim),
    StringConstraints(min_length=1, max_length = 200)
]

DescriptionRule = Annotated[
    str,
    BeforeValidator(_trim),
    StringConstraints(min_length=1, max_length = 2000)
]

OptionalDescriptionRule = Annotated[
    Optional[str],
    BeforeValidator(_none_if_empty),
    StringConstraints(min_length=1, max_length = 2000)
]