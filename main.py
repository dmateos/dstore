import fastapi
import pydantic
import typing
import redis
import secrets


class Blob(pydantic.BaseModel):
    data: str
    lifetime: int


class BlobException(Exception):
    pass


class BlobStorage:
    def __init__(self):
        self.engine = redis.Redis(host="redis0.mateos.lan", port=6379)

    def save(self, key: str, value: str) -> str:
        try:
            if key == "auto":
                k = self._random_key()
                self.engine.set(k, value)
                return k
            else:
                self.engine.set(key, value)
                return key

        except Exception:
            raise BlobException("could not get value")

    def get(self, key: str) -> str:
        try:
            data = self.engine.get(key)
            if data is not None:
                return data
            else:
                raise BlobException("could not set value")
        except Exception:
            raise BlobException("could not set value")

    def _random_key(self) -> str:
        random = secrets.token_hex(3)

        if self.engine.exists(random):
            return self._random_key()
        else:
            return random


app = fastapi.FastAPI()
storage = BlobStorage()


@app.get("/{blob_handle}")
def get_blob(blob_handle: str, q: typing.Optional[str] = None):
    try:
        data = storage.get(blob_handle)
        return {"data": data}
    except BlobException:
        raise fastapi.HTTPException(status_code=404, detail="blob not found")


@app.post("/{blob_handle}")
def push_blob(blob_handle: str, blob: Blob):
    try:
        handle = storage.save(blob_handle, blob.data)
        return {"id": handle}
    except BlobException:
        raise fastapi.HTTPException(status_code=403, detail="blob exists")
