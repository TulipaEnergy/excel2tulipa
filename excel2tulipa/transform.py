"""Extract and transform from Excel to `DataFrame`."""

from dataclasses import asdict
from pathlib import Path

import duckdb
import pandas as pd

from .config import Section


def read_section(fname: str | Path, opts: Section) -> pd.DataFrame:
    """Read a DataFrame from Excel as per options."""
    df = pd.read_excel(fname, **asdict(opts.excel))

    if opts.renames:
        df.index.names = [
            new for old, new in opts.renames if (old if old else None) in df.index.names
        ]

    if opts.unpivot:
        cols = df.columns
        if opts.unpivot_has_dupes and cols.dtype in [object, "string"]:  # noqa: E721
            cols = df.columns.str.extract(r"^(.+)(\.[0-9]+)$")[0]
            if not cols.isna().any():
                df.columns = (
                    cols.astype(opts.unpivot_var_type)
                    if opts.unpivot_var_type
                    else cols
                )
        df = (
            df.melt(**asdict(opts.unpivot))
            .set_index(opts.unpivot.var_name, append=True)
            .rename({"value": opts.name}, axis=1)
        )
    return df


def combine_sections(
    dbfile: str | Path, tblname: str, fname: str | Path, opts: list[Section]
):
    """Combine sections into a multicolumn table."""
    df = pd.concat(
        [read_section(fname, option) for option in opts], axis=1
    ).reset_index()
    with duckdb.connect(dbfile) as con:
        con.register("df", df)
        con.sql(f"CREATE TABLE {tblname} AS SELECT * FROM df")
