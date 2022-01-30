#!/bin/env python3

from enum import Enum
import strictyaml
from strictyaml import Map, Seq, UniqueSeq, EmptyList, Int, Str, Optional

__all__ = ['schema', 'Format', 'InputFormat']

class Format(Enum):
    """
    Enum for the different output formats.
    """
    RENDER = 'render'
    DATA = 'data'

class InputFormat(Enum):
    """
    Enum for the different input formats.
    """
    YAML = 'yaml'
    TXT = 'txt'

formats = strictyaml.Enum(list([e.value for e in Format]))

schema = Map({
    "keys": Seq(Map({
        "key": Str(),
        "seq": Seq(Int()),
        Optional("ignore", default=[]): EmptyList() | UniqueSeq(formats),
        Optional("svg", default=""): Str(),
    })),
})
