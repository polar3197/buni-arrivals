# The data

Everything under `data/` stays on your machine (it's in `.gitignore`).

```
data/
  raw/511/2026-09-so.zip   one month from 511, untouched (scripts/fetch_511_history.py)
  processed/               what you build from it (e.g. segments.parquet)
```

## What's in a month's file

`2026-09-so.zip` is 575 MB zipped, 3.4 GB unzipped. It covers **every Bay Area transit agency**: Muni's rows are the ones with `agency_id` `SF` (and IDs start with `SF:`).

| File | What it is |
|---|---|
| `stop_observations.txt` (2.9 GB) | One row per vehicle reaching a stop: **when it actually arrived**, and when the timetable said it would |
| `trips.txt`, `stop_times.txt`, `stops.txt`, `routes.txt`, `calendar_dates.txt` | That month's timetable (GTFS, the standard timetable format) for all agencies |
| `directions.txt`, `transfers.txt`, `pathways.txt`, `levels.txt`, `agency.txt` | Supporting timetable files you probably won't need |

### `stop_observations.txt` columns

| Column | Meaning |
|---|---|
| `trip_id` | The trip (e.g. `SF:12108780_M11:20260930`) |
| `service_date` | The service day, `YYYYMMDD` |
| `vehicle_id` | The bus or train |
| `stop_sequence` | This stop's place in the trip (1, 2, 3, ...) |
| `observed_arrival_time` | When it actually got there, `HH:MM:SS` local time. Hours can pass 24 for trips that run past midnight |
| `observed_departure_time` | Same as arrival in this data |
| `dwell_time_secs` | Always 0 here, so how long it waited at the stop is unknown |
| `route_id`, `agency_id`, `direction_id` | Which line, which agency, which way |
| `from_stop_id`, `to_stop_id` | The previous stop and this stop: the segment just driven (from is blank on a trip's first stop) |
| `scheduled_arrival_time` | When the timetable said it would arrive |

The rest (`trip_start_time`, `schedule_relationship`, `uncertainty`, `scheduled_dwell_time_secs`, `scheduled_departure_time`) are mostly blank or constant for Muni.

### Things to watch for

- **Times are local and can pass 24:00.** A trip that starts at 11:50 PM keeps counting: `24:15:00` is 12:15 AM the next calendar day, still on the same `service_date`.
- **Daylight saving.** GTFS times count from noon minus 12 hours, which is midnight except on the two change days a year.
- **Distances** between stops come from `shape_dist_traveled` in `stop_times.txt` (distance along the route), or from the stops' coordinates as a fallback.
- **Messy rows.** Expect missing stops, repeated rows, and impossible values (negative or hours-long segments).

## Getting more months

Put your 511 key in a file named `.env` at the repo root:

```
API_KEY_511=your-key-here
```

then:

```
python scripts/fetch_511_history.py 2026-08
```

Each month is one request against 511's limit of 60 per hour per key. History goes back to March 2022.

## License

Transit data provided by 511.org. Its open data license allows storing the data and publishing work derived from it, with that credit shown.
