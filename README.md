# excel2tulipa

A configurable generic tool to import data from Excel files to a
DuckDB database file.

## Example use

```python
In [1]: from excel2tulipa.config import read_conf

In [2]: from excel2tulipa.transform import combine_sections

In [3]: conf = read_conf("etc/reader_spec.toml")

In [4]: combine_sections("test.db", "technologies", "data/main.xlsx", conf["technologies"])
```

```
$ duckdb test.db
D .tables
technologies
D SELECT * FROM technologies LIMIT 7;
┌──────────┬────────────────┬─────────────────┬────────────┬───────────────┐
│ tech_id  │ milestone_year │ investment_cost │ fixed_cost │ variable_cost │
│ varchar  │     int64      │     double      │   double   │    double     │
├──────────┼────────────────┼─────────────────┼────────────┼───────────────┤
│ Res01_01 │           2020 │             0.0 │        0.0 │           0.0 │
│ Res01_02 │           2020 │             0.5 │        0.0 │           0.0 │
│ Res02_01 │           2020 │             0.0 │        0.0 │           0.0 │
│ Res02_02 │           2020 │            2.37 │        0.0 │           0.0 │
│ Res02_03 │           2020 │             8.2 │        0.0 │           0.0 │
│ Res02_04 │           2020 │           10.37 │        0.0 │           0.0 │
│ Res02_05 │           2020 │           12.26 │        0.0 │           0.0 │
└──────────┴────────────────┴─────────────────┴────────────┴───────────────┘
```
