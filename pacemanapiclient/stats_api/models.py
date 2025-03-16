import typing as t

from pydantic import BaseModel, RootModel

Split = t.Literal[
    "nether",
    "bastion",
    "fortress",
    "first_structure",
    "second_structure",
    "first_portal",
    "stronghold",
    "end",
    "finish",
]


class SplitStats(BaseModel):
    count: int
    avg: str


class SessionStats(BaseModel):
    nether: SplitStats
    bastion: SplitStats
    fortress: SplitStats
    first_portal: SplitStats
    stronghold: SplitStats
    end: SplitStats
    finish: SplitStats


class WorldData(BaseModel):
    id: int  # run id from stats db
    worldId: str  # world id from paceman api (hash of world file path)
    nickname: str  # mc username
    uuid: str  # mc uuid
    twitch: t.Optional[str]  # twitch account (or null)
    nether: int  # IGT in ms
    bastion: t.Optional[int]  # IGT in ms (or null)
    fortress: t.Optional[int]  # IGT in ms (or null)
    first_portal: t.Optional[int]  # IGT in ms (or null)
    stronghold: t.Optional[int]  # IGT in ms (or null)
    end: t.Optional[int]  # IGT in ms (or null)
    finish: t.Optional[int]  # IGT in ms (or null)
    netherRta: int  # RTA in ms
    bastionRta: t.Optional[int]  # RTA in ms (or null)
    fortressRta: t.Optional[int]  # RTA in ms (or null)
    first_portalRta: t.Optional[int]  # RTA in ms (or null)
    strongholdRta: t.Optional[int]  # RTA in ms (or null)
    endRta: t.Optional[int]  # RTA in ms (or null)
    finishRta: t.Optional[int]  # RTA in ms (or null)
    insertTime: int  # unix timestamp (secs) of nether enter
    updateTime: int  # unix timestamp (secs) of last split update
    vodId: t.Optional[int]  # twitch VOD id (or null)
    vodOffset: t.Optional[int]  # seconds from VOD start to run start (or null)


class World(BaseModel):
    data: WorldData
    time: int  # unix timestamp (ms) when this data was last cached
    isLive: bool  # whether the run is currently in liveruns


class Run(BaseModel):
    id: int  # run id from stats db
    nether: int  # IGT in ms
    bastion: t.Optional[int]  # IGT in ms (or null)
    fortress: t.Optional[int]  # IGT in ms (or null)
    first_portal: t.Optional[int]  # IGT in ms (or null)
    stronghold: t.Optional[int]  # IGT in ms (or null)
    end: t.Optional[int]  # IGT in ms (or null)
    finish: t.Optional[int]  # IGT in ms (or null)
    lootBastion: t.Optional[int]  # IGT in ms (or null)
    obtainObsidian: t.Optional[int]  # IGT in ms (or null)
    obtainCryingObsidian: t.Optional[int]  # IGT in ms (or null)
    obtainRod: t.Optional[int]  # IGT in ms (or null)
    time: int  # unix timestamp (secs) of nether enter


Runs = RootModel[t.List[Run]]

LeaderboardType = t.Literal["count", "average", "fastest", "conversion"]


class Leaderboard(BaseModel):
    uuid: str  # mc uuid
    name: str  # mc username
    value: t.Union[int, float]  # value for given type (nether enter count)
    qty: int  # qty (always present)
    avg: float  # avg (always present)


Leaderboards = RootModel[t.List[Leaderboard]]


class Timestamp(BaseModel):
    id: int  # run id
    runName: str  # last split of run
    start: float  # timestamp of run start (with decimals)
    nether: int  # no decimals sorry
    bastion: t.Optional[float]  # with decimals (or null)
    fortress: t.Optional[float]  # with decimals (or null)
    first_portal: t.Optional[float]  # with decimals (or null)
    stronghold: t.Optional[float]  # with decimals (or null)
    end: t.Optional[float]  # with decimals (or null)
    finish: t.Optional[float]  # with decimals (or null)
    realUpdate: t.Optional[
        t.Union[int, float]
    ]  # more accurate but nullable, no decimals
    lastUpdated: t.Union[
        int, float
    ]  # always exists but affected by db patches, no decimals


Timestamps = RootModel[t.List[Timestamp]]
