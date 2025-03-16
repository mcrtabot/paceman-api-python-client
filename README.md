PaceMan API Python Client

## Install

```shell
$ pip install git+https://github.com/mcrtabot/paceman-api-python-client.git
```

## Usage

```python
from pacemanapiclient import PacemanAPIClient, PacemanStatsAPIClient

client = PacemanAPIClient()
live_runs = client.get_liveruns()
for run in live_runs.root:
    print(run)

stats_client = PacemanStatsAPIClient()
timestamps = stats_client.get_recent_timestamps("mcrtabot")
for timestamp in timestamps.root:
    print(timestamp)
```

## API Document

### PacemanAPIClient

No Document

### PacemanStatsClient

https://paceman.gg/stats/api/
