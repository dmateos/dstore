import fastapi
import pydantic
import typing
import redis


class Blob(pydantic.BaseModel):
    handle: str
    data: str
    lifetime: int


class BlobException(Exception):
    pass


class BlobStorage:
    def __init__(self):
        self.engine = redis.Redis(host="redis0.mateos.lan", port=6379)

    def save(self, key, value):
        try:
            self.engine.set(key, value)
        except Exception:
            raise BlobException("could not get value")

    def get(self, key):
        try:
            return self.engine.get(key)
        except Exception:
            raise BlobException("could not set value")


app = fastapi.FastAPI()
storage = BlobStorage()


@app.get("/{blob_handle}")
def get_blob(blob_handle: str, q: typing.Optional[str] = None):
    try:
        print(blob_handle)
        data = storage.get(blob_handle)
        return {"data": data}
    except BlobException:
        raise fastapi.HTTPException(status_code=404, detail="blob not found")


@app.post("/")
def push_blob(blob: Blob):
    try:
        storage.save(blob.handle, blob.data)
        return {"id": blob.handle}
    except BlobException:
        raise fastapi.HTTPException(status_code=403, detail="blob exists")
