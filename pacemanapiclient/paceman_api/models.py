import typing as t
from pydantic import BaseModel, RootModel


class Event(BaseModel):
    eventId: str
    rta: int
    igt: int


class EventList(RootModel[t.List[Event]]):
    pass


class User(BaseModel):
    uuid: str
    liveAccount: t.Optional[str] = None


class ItemData(BaseModel):
    estimatedCounts: t.Dict[str, int]
    usages: t.Dict[str, int]


class LiveRun(BaseModel):
    worldId: str
    gameVersion: str
    eventList: EventList
    contextEventList: EventList
    user: User
    isCheated: bool
    isHidden: bool
    numLeaves: int
    lastUpdated: int
    nickname: str
    itemData: t.Optional[ItemData] = None


LiveRuns = RootModel[t.List[LiveRun]]
