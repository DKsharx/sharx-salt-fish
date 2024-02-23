import os
import shutil
import subprocess
import threading
import tkinter.messagebox
from enum import Enum

import requests
from packaging.version import parse
from tqdm import tqdm

from script.utils.config import ConfigUtil, ConfigConstants
from script.utils.logger.logger import logger
from script.utils.update.FastestMirror import FastestMirror
import re
import markdown


class UpdateStatus(Enum):
    SUCCESS = 1
    UPDATE_AVAILABLE = 2
    FAILURE = 0


class AppUpdateHandler:
    def __init__(self):
        self.state = UpdateStatus.SUCCESS

    def remove_images_from_markdown(self, markdown_content):
        # 定义匹配Markdown图片标记的正则表达式
        img_pattern = re.compile(r'!\[.*?\]\(.*?\)')

        # 使用sub方法替换所有匹配的图片标记为空字符串
        cleaned_content = img_pattern.sub('', markdown_content)

        return cleaned_content

    def check_update(self):
        try:
            response = requests.get(FastestMirror.get_github_api_mirror("DKsharx", "sharx-salt-fish"),
                                    timeout=10, headers=ConfigUtil.get_useragent())
            response.raise_for_status()

            data = response.json()[0]
            version = data["tag_name"]

            content = self.remove_images_from_markdown(data["body"])

            assert_url = None
            for asset in data["assets"]:
                if (ConfigUtil.get_value(ConfigConstants.update_full_enable_key) and
                    "full" in asset["browser_download_url"]) or \
                        (not ConfigUtil.get_value(ConfigConstants.update_full_enable_key)
                         and "full" not in asset["browser_download_url"]):
                    assert_url = asset["browser_download_url"]
                    break
            if assert_url is None:
                self.state = UpdateStatus.SUCCESS
                return

            cVersion = ConfigUtil.get_app_version()
            if parse(version.lstrip('v')) > parse(cVersion.lstrip('v')):
                self.title = f"发现新版本：{cVersion} ——> {version})"
                self.content = markdown.markdown(content)
                self.download_url = assert_url
                self.state = UpdateStatus.UPDATE_AVAILABLE
            else:
                self.state = UpdateStatus.SUCCESS
        except Exception as e:
            logger.info(e)
            self.state = UpdateStatus.FAILURE
        self.start_update()

    def start_update(self):
        def update_function():
            if self.state == UpdateStatus.UPDATE_AVAILABLE:
                result = tkinter.messagebox.askyesno(title=self.title, message=self.content)
                if result:
                    # 更新操作
                    self.run_update()
            elif self.state == UpdateStatus.SUCCESS:
                tkinter.messagebox.showinfo(title='当前已经是最新版本,无需更新', message='')
            else:
                tkinter.messagebox.showwarning(title='检查更新失败QAQ', message='')

        threading.Thread(target=update_function).start()

    def __download_with_progress(self, download_url, save_path):
        if os.path.exists(self.aria2_path):
            if os.path.exists(save_path):
                command = [self.aria2_path, "--max-connection-per-server=16", "--continue=true",
                           f"--dir={os.path.dirname(save_path)}", f"--out={os.path.basename(save_path)}",
                           f"{download_url}"]
            else:
                command = [self.aria2_path, "--max-connection-per-server=16",
                           f"--dir={os.path.dirname(save_path)}", f"--out={os.path.basename(save_path)}",
                           f"{download_url}"]
            process = subprocess.Popen(command)
            process.wait()
            if process.returncode != 0:
                raise Exception
        else:
            # 获取文件大小
            response = requests.head(download_url)
            file_size = int(response.headers.get('Content-Length', -1))

            # 设置请求头，支持断点续传
            headers = {}
            if os.path.exists(save_path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(save_path)

            # 使用 tqdm 创建进度条
            with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                with requests.get(download_url, headers=headers, stream=True) as response:
                    with open(save_path, 'ab' if headers else 'wb') as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                                pbar.update(len(chunk))

    def __download_file(self):
        self.temp_path = os.path.abspath("./temp")
        self.download_file_path = os.path.join(self.temp_path, os.path.basename(self.download_url))
        logger.info("开始下载...")
        while True:
            try:
                self.__download_with_progress(self.download_url, self.download_file_path)
                logger.info(f"下载完成：{self.download_file_path}")
                break
            except Exception as e:
                logger.info(f"下载失败：{e}")

    def __extract_file(self):
        logger.info("开始解压...")
        self.exe_path = os.path.abspath("./assets/7z/7za.exe")
        self.extract_folder_path = os.path.join(self.temp_path, os.path.basename(self.download_url).rsplit(".", 1)[0])
        while True:
            try:
                if os.path.exists(self.exe_path):
                    if not subprocess.run([self.exe_path, "x", self.download_file_path, f"-o{self.temp_path}", "-aoa"],
                                          check=True):
                        raise Exception
                else:
                    shutil.unpack_archive(self.download_file_path, self.temp_path)
                logger.info(f"解压完成：{self.extract_folder_path}")
                break
            except Exception as e:
                logger.info(f"解压失败：{e}")

    def __cover_folder(self):
        logger.info("开始覆盖...")
        self.cover_folder_path = os.path.abspath("./")
        while True:
            try:
                shutil.copytree(self.extract_folder_path, self.cover_folder_path, dirs_exist_ok=True)
                logger.info(f"覆盖完成：{self.cover_folder_path}")
                break
            except Exception as e:
                logger.info(f"覆盖失败：{e}")

    def __delete_files(self):
        logger.info("开始清理...")
        try:
            os.remove(self.download_file_path)
            logger.info(f"清理完成：{self.download_file_path}")
        except Exception as e:
            logger.info(f"清理失败：{e}")
        try:
            shutil.rmtree(self.extract_folder_path)
            logger.info(f"清理完成：{self.extract_folder_path}")
        except Exception as e:
            logger.info(f"清理失败：{e}")

    def run_update(self):

        self.__download_file()

        self.__extract_file()

        self.__cover_folder()

        self.__delete_files()

        logger.info("已更新成功,请重启本软件❥(^_-)")
