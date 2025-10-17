import os, uuid, pathlib, shutil
from typing import BinaryIO, Tuple

class IStorage:
    def save(self, file: BinaryIO, *, mime: str, ext: str | None) -> tuple[str, str]:
        """Сохраняет файл и возвращает (uid, public_url)"""
        raise NotImplementedError

    def path_for(self, uid: str) -> str:
        raise NotImplementedError

class LocalFileStorage(IStorage):
    def __init__(self, root: str = "/data/media", public_prefix: str = "/media"):
        self.root = pathlib.Path(root)
        self.prefix = public_prefix
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, file: BinaryIO, *, mime: str, ext: str | None) -> tuple[str, str]:
        uid = uuid.uuid4().hex
        filename = f"{uid}{('.' + ext) if ext else ''}"
        target = self.root / filename
        with open(target, "wb") as out:
            shutil.copyfileobj(file, out)
        return uid, f"{self.prefix}/{uid}"

    def path_for(self, uid: str) -> str:
        # ищем файл по uid.* (расширение неизвестно)
        for p in self.root.glob(f"{uid}*"):
            return str(p)
        # если не нашли, вернем путь по умолчанию без расширения
        return str(self.root / uid)