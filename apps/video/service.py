import os.path
import shutil

from service.multipart_file_upload import MultipartFileUploadService


class VideoUploadService(MultipartFileUploadService):
    def move_to_db_dictionary(self, origin_video_path: str):
        target_dir = self._get_upload_dir("videos")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        target_path = shutil.move(origin_video_path, target_dir)
        return target_path
