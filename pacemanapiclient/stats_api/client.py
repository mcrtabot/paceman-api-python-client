import typing as t

from ..base_client import BaseApiClient
from .models import (
    Leaderboards,
    Runs,
    SessionStats,
    Split,
    SplitStats,
    Timestamps,
    World,
)


class PacemanStatsAPIClient(BaseApiClient):
    BASE_URL: str = "https://paceman.gg/stats/api/"

    def get_session_nethers(
        self, name: str, hours: int = 24, hours_between: int = 6
    ) -> SplitStats:
        """Returns nether enter count & average for a given timeframe

        Parameters
        ----------
        name : str
            Either MC username or twitch
        hours : int, optional
            How many hours of stats to include (default: 24)
        hours_between : int, optional
            The max number of hours between runs in a session (default: 6)

        Returns
        -------
        SplitStats
            Nether enter count & average for a given timeframe

        Caching
        -------
        * 20 seconds
        * There are no rate limits currently, but don't bother spamming this endpoint more than once every 20 seconds
        """
        params = {
            "name": name,
            "hours": hours,
            "hoursBetween": hours_between,
        }
        return SplitStats.model_validate(
            self._make_request("getSessionNethers", params)
        )

    def get_session_stats(
        self, name: str, hours: int = 24, hours_between: int = 6
    ) -> SessionStats:
        """Returns counts & average for all splits in a given timeframe

        Parameters
        ----------
        name : str
            Either MC username or twitch
        hours : int, optional
            How many hours of stats to include (default: 24)
        hours_between : int, optional
            The max number of hours between runs in a session (default: 6)

        Returns
        -------
        SessionStats
            Counts & average for all splits in a given timeframe

        Caching
        -------
        * 20 seconds
        * There are no rate limits currently, but don't bother spamming this endpoint more than once every 20 seconds

        Notes
        -----
        * first_structure and second_structure are recommended instead of bastion and fortress
        * second_structure requires either a rod if fort first, or >50 seconds between structures if bastion first
        """
        params = {
            "name": name,
            "hours": hours,
            "hoursBetween": hours_between,
        }
        response_data = self._make_request("getSessionStats", params)
        return SessionStats.model_validate(response_data)

    def get_split_stats(
        self,
        name: str,
        split: Split,
        hours: int = 24,
        hours_between: int = 6,
        max_time: t.Optional[int] = None,
    ) -> SplitStats:
        """Returns count & average for a given split in a given timeframe

        Parameters
        ----------
        name : str
            Either MC username or twitch
        split : Split
            How many hours of stats to include (default: 24)
        hours : int, optional
            The max number of hours between runs in a session (default: 6)
        hours_between : int, optional
            The split to get stats for (nether, bastion, fortress, first_structure, second_structure, first_portal, stronghold, end, finish)
        max_time : int | None, optional
            The slowest run to include in the average, in milliseconds

        Returns
        -------
        SplitStats
            Count & average for a given split in a given timeframe

        Caching
        -------
        * 20 seconds
        * There are no rate limits currently, but don't bother spamming this endpoint more than once every 20 seconds

        Notes
        -----
        * first_structure and second_structure are recommended instead of bastion and fortress
        * second_structure requires either a rod if fort first, or >50 seconds between structures if bastion first
        """
        params = {
            "name": name,
            "split": split,
            "hours": hours,
            "hoursBetween": hours_between,
        }
        if max_time is not None:
            params["maxTime"] = max_time
        return SplitStats.model_validate(self._make_request("getSplitStats", params))

    def get_world(self, world_id: str) -> t.Optional[World]:
        """Returns data for a given run

        Parameters
        ----------
        world_id : str
            Either a numerical run ID, or the world ID hash

        Returns
        -------
        World | None
            Data for a given run

        Caching
        -------
        * 5 seconds
        * There are no rate limits currently, but don't bother spamming this endpoint more than once every 5 seconds

        Notes
        -----
        * If you need to constantly update splits for a run, consider liveruns (https://paceman.gg/api/ars/liveruns) instead
        """
        params = {"worldId": world_id}
        response_data = self._make_request("getWorld", params)
        if response_data is None:
            return None
        return World.model_validate(self._make_request("getWorld", params))

    def get_recent_runs(
        self, name: str, hours: int = 24, hours_between: int = 6, limit: int = 10
    ) -> Runs:
        """Returns recent runs for a user

        Parameters
        ----------
        name : str
            Either MC username or twitch
        hours : int, optional
            How many hours of stats to include (default: 24)
        hours_between : int, optional
            The max number of hours between runs in a session (default: 6)
        limit : int, optional
            Max number of runs to return (default: 10)

        Returns
        -------
        Runs
            Recent runs for a user

        Caching
        -------
        * 20 seconds
        * There are no rate limits currently, but don't bother spamming this endpoint more than once every 20 seconds

        Notes
        -----
        * If you need more details, such as RTA splits and VOD info, pass the run ID to getWorld
        """
        params = {
            "name": name,
            "hours": hours,
            "hoursBetween": hours_between,
            "limit": limit,
        }
        return Runs.model_validate(self._make_request("getRecentRuns", params))

    def get_leaderboard(
        self,
        days: t.Literal[1, 7, 30, 9999] = 30,
        category: Split = "nether",
        type: t.Literal["count", "average", "fastest", "coversion"] = "count",
        limit: int = 10,
    ) -> Leaderboards:
        """Returns the leaderboard for a given category and type

        Parameters
        ----------
        days : int, optional
            How many days of stats to include (default: 30)
            Valid values: 1, 7, 30, 9999
        category : Split, optional
            Which split to get results for (default: nether)
            Valid values: nether, bastion, fortress, first_structure, second_structure, first_portal, second_portal, stronghold, end, finish
        type : LeaderboardType, optional
            Method of comparing values (default: count)
            Valid values: count, average, fastest, conversion
        limit : int, optional
            Max number of players to return (default: 10, max: 999999)

        Returns
        -------
        Leaderboards
            The leaderboard for a given category and type

        Caching
        -------
        * 10 minutes
        * There are no rate limits currently, but don't bother spamming this endpoint more than once every 10 minutes

        Notes
        -----
        * Avoid using this if you can use getSessionStats instead.
        * getLeaderboard requires parsing all runs from all users during the given timeframe
        """
        params = {
            "days": days,
            "category": category,
            "type": type,
            "limit": limit,
        }
        return Leaderboards.model_validate(self._make_request("getLeaderboard", params))

    def get_recent_timestamps(
        self, name: str, limit: int = 20, onlyFort: bool = False
    ) -> Timestamps:
        """Returns unix timestamps for splits in recent runs

        Parameters
        ----------
        name : str
            Either MC username or twitch
        limit : int, optional
            Max number of runs to return (default: 20, max: 50)
        onlyFort : bool, optional
            Whether to only include runs that have 2 structures (default: false)

        Returns
        -------
        Timestamps
            Unix timestamps for splits in recent runs

        Caching
        -------
        * 10 seconds
        * There are no rate limits currently, but don't bother spamming this endpoint more than once every 10 seconds

        Notes
        -----
        * Intended use case is clipping runs from local recordings
        * If you want IGT/RTA split info, use getRecentRuns instead.
        """

        params = {
            "name": name,
            "limit": limit,
            "onlyFort": "true" if onlyFort else "false",
        }
        return Timestamps.model_validate(
            self._make_request("getRecentTimestamps", params)
        )
