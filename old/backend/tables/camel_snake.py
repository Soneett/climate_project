import re


class CamelToSnake:
    pat = re.compile(r"(?<!^)(?=[A-Z])")

    @classmethod
    def convert(cls, s: str) -> str:
        return re.sub(cls.pat, "_", s).lower()


class SnakeToCamel:
    @classmethod
    def convert(cls, s: str) -> str:
        return "".join(map(lambda x: x.capitalize(), s.split("_")))
