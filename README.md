# excel2tulipa

A configurable generic tool to import data from Excel files to a
DuckDB database file.

## Config

```toml
[table_name]
name = "value_column"  # after unpivot, ignored otherwise
renames = [
  ["old1", "new1"],
  ["", "newname"]
]

# if unpivoted column names occur more than once
unpivot_has_dupes = true
# data type of the unpivoted column
unpivot_var_type = 'type_name'

# options passed on to `pandas.read_excel`;
# see https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
[table_name.excel]
...


# options passed on to `pandas.melt`;
# see https://pandas.pydata.org/docs/reference/api/pandas.melt.html
[table_name.unpivot]
...

# array, to be collated into one table
[[another_table]]
name = "default"  # special section, default values for the array
```

## Example use

```
$ python -m excel2tulipa -c etc/reader_spec.toml -d test.db data/main.xlsx
$ duckdb test.db
v1.2.1 8e52ec4395
Enter .help for usage hints.
D .tables
consumers            technologies         technology_metadata
D SELECT * FROM consumers LIMIT 3;
┌──────────────────────────────────┬───────────┬───────────────┬────────────────┬────────┐
│             consumer             │   unit    │ consumer_type │ milestone_year │ demand │
│             varchar              │  varchar  │    varchar    │     int64      │ double │
├──────────────────────────────────┼───────────┼───────────────┼────────────────┼────────┤
│ Electricity demand - Residential │ [PJ]      │ Driver        │           2020 │   84.0 │
│ Houses - Residential Flats       │ [khouses] │ Driver        │           2020 │ 2900.0 │
│ Houses - Residential Terrace     │ [khouses] │ Driver        │           2020 │ 2400.0 │
└──────────────────────────────────┴───────────┴───────────────┴────────────────┴────────┘
D SELECT * FROM technology_metadata LIMIT 3;
┌──────────┬───────────────────┬──────────┬─────────────┬────────────┬──────────────────────────────────┬─────────────────────────────────────────────────────────┬─────────────┐
│ Tech_ID  │  Policy Sectors   │ Category │   Sector    │ Sub-sector │          Main Activity           │                          Name                           │     UoC     │
│ varchar  │      varchar      │ varchar  │   varchar   │  varchar   │             varchar              │                         varchar                         │   varchar   │
├──────────┼───────────────────┼──────────┼─────────────┼────────────┼──────────────────────────────────┼─────────────────────────────────────────────────────────┼─────────────┤
│ Res01_01 │ Gebouwde omgeving │ Final    │ Residential │ Appliances │ Electricity demand - Residential │ Dummy standard electricity consumption - Residential    │ [PJ/y]      │
│ Res01_02 │ Gebouwde omgeving │ Final    │ Residential │ Appliances │ Electricity demand - Residential │ Flexible standard electricity consumption - Residential │ [PJ/y]      │
│ Res02_01 │ Gebouwde omgeving │ Final    │ Residential │ Flats      │ Houses - Residential Flats       │ House with insulation GFE - Residential Flats           │ [khouses/y] │
└──────────┴───────────────────┴──────────┴─────────────┴────────────┴──────────────────────────────────┴─────────────────────────────────────────────────────────┴─────────────┘
D SELECT * FROM technologies LIMIT 3;
┌──────────┬────────────────┬─────────────────┬────────────┬───────────────┐
│ tech_id  │ milestone_year │ investment_cost │ fixed_cost │ variable_cost │
│ varchar  │     int64      │     double      │   double   │    double     │
├──────────┼────────────────┼─────────────────┼────────────┼───────────────┤
│ Res01_01 │           2020 │             0.0 │        0.0 │           0.0 │
│ Res01_02 │           2020 │             0.5 │        0.0 │           0.0 │
│ Res02_01 │           2020 │             0.0 │        0.0 │           0.0 │
└──────────┴────────────────┴─────────────────┴────────────┴───────────────┘
```
