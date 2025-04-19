"""TOML config."""

from dataclasses import asdict, dataclass, field, is_dataclass
from pathlib import Path
import tomllib
from types import UnionType
from typing import Type, TypeVar, get_args, get_origin, no_type_check

from rich.pretty import pprint
from rich.console import Console


def pretty_str(data) -> str:
    console = Console()
    with console.capture() as cap:
        console.print(data)
    return cap.get()


T = TypeVar("T")


def unguarded_is_dataclass(_type: Type[T], /) -> bool:
    """Remove :ref:`TypeGuard` from is_dataclass.

    see: https://github.com/python/mypy/issues/14941
    """
    return is_dataclass(_type)


@no_type_check
def unwrap_unions(_type: type | UnionType) -> tuple[type, ...]:
    """Unwrap Union types into its constituents."""
    return get_args(_type) if get_origin(_type) is UnionType else (_type,)


@dataclass(frozen=True)
class Excel:
    """Options for pandas.read_excel."""

    sheet_name: str
    usecols: str
    index_col: list[int] | int | None = None
    header: list[int] | int | None = None
    skiprows: list[int] | int | None = None


@dataclass(frozen=True)
class Unpivot:
    """Options for pandas.melt."""

    var_name: str
    ignore_index: bool | None = None


@dataclass(frozen=True)
class Section:
    """Options for reading a column/table."""

    name: str
    excel: Excel
    renames: list[list[str]] = field(default_factory=list)
    unpivot: Unpivot | None = None
    unpivot_has_dupes: bool | None = None
    unpivot_var_type: str | None = None

    def __post_init__(self):
        """Set nested options."""
        for key, field_t in self.__annotations__.items():
            value = getattr(self, key)
            for _type in unwrap_unions(field_t):
                if unguarded_is_dataclass(_type) and isinstance(value, dict):
                    super().__setattr__(key, _type(**value))

    def asdict(self):
        """Convert dataclass to `dict`."""
        return {
            k: asdict(v) if unguarded_is_dataclass(v) else v
            for k, v in asdict(self).items()
        }

    # def __repr__(self):
    #     """Repr as dict."""
    #     return f"{self.asdict()}"


def sections_w_defaults(subsections: list[dict]) -> list[dict]:
    """Create set of Section objects merging w/ defaults."""
    default = dict(*filter(lambda i: i.get("name") == "default", subsections))
    default.pop("name")
    table = []
    for subsection in subsections:
        if (name := subsection.get("name")) is None or name == "default":
            continue
        col_opts = {}
        for k, v in subsection.items():
            match v:
                case dict():
                    col_opts[k] = {**default.get(k, {}), **v}
                case _:
                    col_opts[k] = v
        for k in default:
            if k in col_opts:
                continue
            col_opts[k] = default[k]
        table.append(Section(**col_opts))
    return table


def read_conf(fname: str | Path) -> dict:
    """Read config file, merging w/ defaults."""
    fname = Path(fname)
    conf = tomllib.loads(fname.read_text())
    tables = {}
    for tbl, val in conf.items():
        match val:
            case [dict(), *_]:
                tables[tbl] = sections_w_defaults(val)
            case dict():
                tables[tbl] = Section(**val)
            case _:
                tables[tbl] = val
    return tables
