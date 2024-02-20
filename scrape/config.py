from typing import Annotated

from pydantic import (
    BaseModel,
    NonNegativeInt,
    SecretStr,
    Strict,
    StringConstraints,
)


class StrippedSecretStr(SecretStr):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._secret_value = self._secret_value.strip()


class Config(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True)]
    password: StrippedSecretStr | None
    verbosity: Annotated[NonNegativeInt, Strict] = 1
    save_outputs: bool | None = True
