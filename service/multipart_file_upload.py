import os
import shutil
import time

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

# from django.conf import settings

TMP_UPLOAD_ROOT = settings.TMP_UPLOAD_ROOT
MIDEA_ROOT = settings.MEDIA_ROOT
# tmp_upload_root = r'F:\resource\target'
IO_SIZE = 1024 * 1024  # 每次IO操作1mb数据


class MultipartFileUploadService:

    def _get_chunk_dir(self, file_hash: str):
        return os.path.join(TMP_UPLOAD_ROOT, f'chunkDir_{file_hash}')

    def _get_file_path(self, file_hash: str, file_ext: str):
        return os.path.join(TMP_UPLOAD_ROOT, f"{file_hash}{file_ext}")

    def _get_upload_dir(self, root_path_prefix="tmp"):
        """
        获取应该存储到数据库中的目录位置

        目录不一定存在，可能需要手动创建
        :param root_path_prefix: 目录路径的可选前缀，如"videos", ”images“
        :return: 目录路径
        """
        path_sep = os.path.sep
        sub_dir = time.strftime("%Y/%m/%d/%H/%M".replace("/", path_sep), time.localtime())
        return os.path.join(MIDEA_ROOT, root_path_prefix, sub_dir)

    def get_uploaded_chunk_list(self, file_hash: str):
        chunk_dir = self._get_chunk_dir(file_hash)
        return os.listdir(chunk_dir) if os.path.exists(chunk_dir) else []

    def merge_file_chunk(self, file_hash: str, file_ext: str):
        file_path = self._get_file_path(file_hash, file_ext)
        chunk_dir = self._get_chunk_dir(file_hash)
        if not os.path.exists(chunk_dir):
            raise FileNotFoundError('chunk dictionary not exists.')
        chunk_path_list = [(os.path.join(chunk_dir, chunk_name), int(chunk_name.split('-')[-1])) for chunk_name in
                           os.listdir(chunk_dir)]
        # 将切片按顺序排序，否则拼接的时候会错位
        chunk_path_list.sort(key=lambda item: item[1])
        with open(file_path, 'ab') as write_stream:
            for chunk_path, chunk_index in chunk_path_list:
                with open(chunk_path, 'rb') as read_stream:
                    while True:
                        data = read_stream.read(IO_SIZE)
                        if not data:
                            break
                        write_stream.write(data)

        # 合并完成删除切片
        shutil.rmtree(chunk_dir)
        return file_path

    def upload_file_chunk(self, chunk: UploadedFile, chunk_name: str, file_hash: str, file_ext: str) -> None:
        file_path = os.path.join(TMP_UPLOAD_ROOT, f"{file_hash}{file_ext}")

        chunk_dir = self._get_chunk_dir(file_hash)
        chunk_path = os.path.join(chunk_dir, chunk_name)

        if os.path.exists(file_path):
            return
        if os.path.exists(chunk_path):
            return

        if not os.path.exists(chunk_dir):
            os.makedirs(chunk_dir)

        with open(chunk_path, 'wb') as f:
            for chunk_data in chunk.chunks():
                f.write(chunk_data)

    def verify_should_upload(self, file_hash: str, file_ext: str):
        file_path = os.path.join(TMP_UPLOAD_ROOT, f"{file_hash}{file_ext}")
        if os.path.exists(file_path):
            return {
                'shouldUpload': False
            }
        else:
            uploaded_chunk_list = self.get_uploaded_chunk_list(file_hash)
            return {
                'shouldUpload': True,
                'uploadedList': uploaded_chunk_list
            }
