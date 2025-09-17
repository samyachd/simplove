# profiles/storage_backends.py
from django.core.files.storage import Storage
from django.conf import settings
from django.utils.deconstruct import deconstructible
from utils.supabase_client import get_supabase
import mimetypes
import os
from supabase import StorageException


@deconstructible
class SupabaseMediaStorage(Storage):
    """
    Backend de stockage pour Supabase Storage.
    Utilise l'URL publique du bucket pour accéder aux fichiers.
    """

    bucket_name = settings.SUPABASE_BUCKET

    def __init__(self, bucket=None):
        super().__init__()
        if bucket:
            self.bucket_name = bucket
        self.client = get_supabase().storage
        print(f"[SupabaseMediaStorage] INIT bucket = {self.bucket_name}")

        # URL publique de base pour le bucket
        self.public_url_base = getattr(settings, "SUPABASE_PUBLIC_URL", None)
        if not self.public_url_base:
            self.public_url_base = (
                f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket_name}"
            )

    def _save(self, name, content):
        content.open()
        data = content.read()
        mime, _ = mimetypes.guess_type(name)
        path = name.lstrip("/")

        try:
            self.client.from_(self.bucket_name).upload(
                path=path,
                file=data,
                file_options={"upsert": "true"},
            )
            print(f"[Supabase] upload OK: {name}")
        except StorageException as e:
            print(f"[Supabase] upload ERROR: {e}")
            if "Duplicate" not in str(e):
                raise
        return name

    def _open(self, name, mode="rb"):
        raise NotImplementedError("L'ouverture directe n'est pas supportée.")

    def delete(self, name):
        path = name.lstrip("/")
        try:
            self.client.from_(self.bucket_name).remove([path])
        except StorageException as e:
            print(f"[Supabase] delete ERROR: {e}")

    def exists(self, name):
        path = name.lstrip("/")
        try:
            files = self.client.from_(self.bucket_name).list(path=os.path.dirname(path))
            return any(f["name"] == os.path.basename(path) for f in files)
        except StorageException:
            try:
                self.client.from_(self.bucket_name).download(path)
                return True
            except StorageException:
                return False

    def url(self, name):
        """
        Renvoie l'URL publique directe depuis Supabase.
        """
        name = name.lstrip("/")
        return f"{self.public_url_base}/{name}"
