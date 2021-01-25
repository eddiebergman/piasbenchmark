# https://stackoverflow.com/a/33533514/5332072
from __future__ import annotations

import os
from abc import abstractmethod
from typing import Mapping, Dict, Any, Tuple, Type

from slurmjobmanager import Job

class BenchmarkJob(Job):

    @abstractmethod
    def __init__(
            self,
            name: str,
            seed: int,
            task: int,
            time: int,
            basedir: str,
            split: Tuple[float, float, float],
            memory: int,
            cpus: int,
            *args,
            **kwargs
    ) -> None:
        super().__init__()
        self._name = name
        self.seed = seed
        self.task = task
        self.split = split
        self.time = time
        self.basedir = basedir
        self.memory = memory
        self.cpus = cpus

    @abstractmethod
    def paths(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def config(self) -> Mapping[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def runner_path(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_config(
        cls,
        cfg: Dict[str, Any],
        basedir: str,
    ) -> BenchmarkJob:
        pass

    def name(self) -> str:
        return self._name

    def ready(self) -> bool:
        return not self.blocked() and not self.complete()
