from typing import TypedDict, Union

# common typings
JsonString = str


class LambdaResponse(TypedDict):
    statusCode: int
    body: Union[str, int]
