from scrape.config import BaseConfig, StrippedStr, StrippedSecretStr


class Config(BaseConfig):
    username: StrippedStr
    password: StrippedSecretStr | None
    save_outputs: bool | None = True
