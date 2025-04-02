#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import requests
import configparser
import shutil
from datetime import datetime
from pathlib import Path
import subprocess
import urllib.request
from typing import Optional

class RulesUpdater:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.temp_dir = self.script_dir / 'temp'
        self.log_dir = self.script_dir / 'log'
        self.config_file = self.script_dir / 'config.ini'
        
        # 设置日志
        self.setup_logging()
        
        # 确保必要目录存在
        self.temp_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        
        # 目标目录（使用环境变量）
        self.mihomo_base = Path(os.getenv('APPDATA')) / 'mihomo-party'
        self.test_dir = self.mihomo_base / 'test'
        self.work_dir = self.mihomo_base / 'work'
        
        # 文件名常量
        self.files = {
            'GEOIP_DAT': 'geoip.dat',
            'GEOSITE_DAT': 'geosite.dat',
            'GEOIP_METADB': 'geoip.metadb',
            'ASN_MMDB': 'ASN.mmdb',
            'COUNTRY_MMDB': 'country.mmdb'
        }
        
        # 读取配置
        self.load_config()

    def setup_logging(self):
        """设置日志系统"""
        log_file = self.log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def load_config(self):
        """加载或创建配置文件"""
        if not self.config_file.exists():
            self.create_default_config()
        
        config = configparser.ConfigParser()
        config.read(self.config_file, encoding='utf-8')
        self.urls = {}
        if 'URLS' in config:
            for key, value in config['URLS'].items():
                self.urls[key.upper()] = value
        else:
            logging.error("配置文件中缺少 [URLS] 部分")
            self.create_default_config()
            config.read(self.config_file, encoding='utf-8')
            self.urls = {key.upper(): value for key, value in config['URLS'].items()}
        
        logging.info("配置文件加载完成")

    def create_default_config(self):
        """创建默认配置文件"""
        config = configparser.ConfigParser()
        config['URLS'] = {
            'GEOIP_URL': 'https://testingcf.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geoip.dat',
            'GEOSITE_URL': 'https://testingcf.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/geosite.dat',
            'GEOIPDB_URL': 'https://testingcf.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geoip.metadb',
            'ASNDB_URL': 'https://gh-proxy.com/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/GeoLite2-ASN.mmdb',
            'COUNTRY_URL': 'https://testingcf.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/country.mmdb'
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        logging.info(f"创建默认配置文件: {self.config_file}")

    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f}{unit}"
            size /= 1024
        return f"{size:.2f}GB"

    def _download_with_requests(self, url: str, output_file: Path) -> bool:
        """使用requests下载"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded_size = 0
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        percent = (downloaded_size / total_size) * 100
                        formatted_total = self._format_size(total_size)
                        formatted_downloaded = self._format_size(downloaded_size)
                        logging.info(f"下载进度: {percent:.1f}% ({formatted_downloaded}/{formatted_total})")
                    else:
                        formatted_downloaded = self._format_size(downloaded_size)
                        logging.info(f"已下载: {formatted_downloaded}")
        return True

    def _download_with_urllib(self, url: str, output_file: Path) -> bool:
        """使用urllib下载"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded_size = 0
            
            with open(output_file, 'wb') as f:
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        percent = (downloaded_size / total_size) * 100
                        formatted_total = self._format_size(total_size)
                        formatted_downloaded = self._format_size(downloaded_size)
                        logging.info(f"下载进度: {percent:.1f}% ({formatted_downloaded}/{formatted_total})")
                    else:
                        formatted_downloaded = self._format_size(downloaded_size)
                        logging.info(f"已下载: {formatted_downloaded}")
        return True

    def _download_with_curl(self, url: str, output_file: Path) -> bool:
        """使用curl下载"""
        try:
            # 使用curl的进度显示功能
            process = subprocess.Popen([
                'curl',
                '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                '-L',
                '--progress-bar',  # 显示进度条
                '--connect-timeout', '30',
                '--retry', '3',
                url,
                '-o', str(output_file)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            # 实时读取curl的输出
            while True:
                line = process.stderr.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    progress = line.strip()
                    if progress:
                        logging.info(f"下载进度: {progress}")
            
            return process.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def download_file(self, url: str, output_file: Path) -> bool:
        """
        使用多种方法尝试下载文件
        """
        temp_file = output_file.with_suffix(output_file.suffix + '.tmp')
        
        # 清理可能存在的临时文件和目标文件
        for file in [temp_file, output_file]:
            try:
                if file.exists():
                    file.unlink()
            except Exception as e:
                logging.error(f"删除文件失败 {file}: {str(e)}")
                return False

        methods = [
            self._download_with_requests,
            self._download_with_urllib,
            self._download_with_curl
        ]

        for method in methods:
            try:
                logging.info(f"尝试使用 {method.__name__} 下载: {url}")
                if method(url, temp_file):
                    try:
                        # 使用shutil.move替代Path.rename，它会自动处理文件替换
                        shutil.move(str(temp_file), str(output_file))
                        logging.info(f"文件下载成功: {output_file}")
                        return True
                    except Exception as e:
                        logging.error(f"移动文件失败 {temp_file} -> {output_file}: {str(e)}")
                        if temp_file.exists():
                            temp_file.unlink()
                        continue
            except Exception as e:
                logging.error(f"下载失败 ({method.__name__}): {str(e)}")
                if temp_file.exists():
                    temp_file.unlink()
                continue

        logging.error(f"所有下载方法均失败: {url}")
        return False

    def update_directory(self, target_dir: Path):
        """更新指定目录的文件"""
        target_dir.mkdir(parents=True, exist_ok=True)
        logging.info(f"开始更新目录: {target_dir}")

        for file_name in self.files.values():
            src = self.temp_dir / file_name
            dst = target_dir / file_name
            try:
                shutil.copy2(src, dst)
                logging.info(f"文件已复制到: {dst}")
            except Exception as e:
                logging.error(f"复制文件失败 {src} -> {dst}: {str(e)}")

    def update_subdirectories(self, parent_dir: Path):
        """更新所有子目录"""
        logging.info("开始更新子目录")
        for subdir in parent_dir.glob('*'):
            if subdir.is_dir():
                self.update_directory(subdir)

    def run(self):
        """运行更新程序"""
        logging.info("====== 开始更新规则文件 ======")
        logging.info(f"目标目录: TEST_DIR={self.test_dir}, WORK_DIR={self.work_dir}")

        # 下载所有文件
        download_success = True
        url_mapping = {
            'GEOIP_DAT': 'GEOIP_URL',
            'GEOSITE_DAT': 'GEOSITE_URL',
            'GEOIP_METADB': 'GEOIPDB_URL',
            'ASN_MMDB': 'ASNDB_URL',
            'COUNTRY_MMDB': 'COUNTRY_URL'
        }

        for file_key, url_key in url_mapping.items():
            if url_key not in self.urls:
                logging.error(f"配置文件中缺少 {url_key}")
                download_success = False
                continue
            
            file_name = self.files[file_key]
            if not self.download_file(self.urls[url_key], self.temp_dir / file_name):
                download_success = False

        if not download_success:
            logging.error("部分文件下载失败，更新终止")
            return False

        # 更新目录
        self.update_directory(self.test_dir)
        self.update_directory(self.work_dir)
        self.update_subdirectories(self.work_dir)

        logging.info("====== 规则文件更新完成 ======")
        return True

if __name__ == '__main__':
    updater = RulesUpdater()
    success = updater.run()
    sys.exit(0 if success else 1) 