class FName:
    Index: int
    Number: int
    String: str
    string: str
    isNone: bool

    def __init__(self, name: str, index: int, number: int) -> None:
        self.string = name
        self.Index = index
        self.Number = number

    @property
    def isNone(self):
        return self.string is None or self.string == "None"

    def GetValue(self):
        return self.string
