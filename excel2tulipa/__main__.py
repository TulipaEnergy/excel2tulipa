from .config import read_conf
from .transform import combine_sections, dfs_to_db, read_section


def write_tbls(dbfile: str, fname: str, conf: dict):
    """Read tables from Excel file, and write to a DuckDB database."""
    dfs = {}
    for section, section_conf in conf.items():
        match section_conf:
            case list():
                dfs[section] = combine_sections(fname, section_conf)
            case _:
                dfs[section] = read_section(fname, section_conf).reset_index()

    dfs_to_db(dfs, dbfile)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("excel_file")
    parser.add_argument("-c", "--config")
    parser.add_argument("-d", "--db")

    opts = parser.parse_args()
    conf = read_conf(opts.config)
    write_tbls(opts.db, opts.excel_file, conf)
