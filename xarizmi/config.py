from typing import Any


class Config:
    _NAME_DOJINESS_THRESHOLD = "DOJINESS_THRESHOLD"

    def __init__(self) -> None:
        self._settings: dict[str, int | float | str | None] = {}
        self.reset()

    def reset(self) -> None:
        self._settings[self._NAME_DOJINESS_THRESHOLD] = 0.95

    @property
    def DOJINESS_THRESHOLD(self) -> float:
        return self._settings.get(Config._NAME_DOJINESS_THRESHOLD)  # type: ignore  # noqa: E501

    @DOJINESS_THRESHOLD.setter
    def DOJINESS_THRESHOLD(self, value: float) -> None:
        self._settings[config._NAME_DOJINESS_THRESHOLD] = value

    def update(self, **kwargs: Any) -> None:
        self._settings.update(kwargs)

    def get(self, key: str) -> int | float | str | None:
        return self._settings.get(key)


# Create a singleton instance of the Config class
config = Config()


def get_config() -> Config:
    global config
    return config


def reset_config() -> None:
    global config
    config.reset()
