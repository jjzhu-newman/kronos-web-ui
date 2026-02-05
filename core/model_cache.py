"""
模型缓存管理模块
实现模型的本地缓存、下载和管理功能
"""

import os
import json
import shutil
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging

try:
    from .logger import get_logger
    logger = get_logger()
except:
    logger = None


def log_info(msg: str):
    if logger:
        logger.info(msg)
    else:
        print(f"[INFO] {msg}")


def log_error(msg: str):
    if logger:
        logger.error(msg)
    else:
        print(f"[ERROR] {msg}")


class ModelCache:
    """模型缓存管理器"""

    def __init__(self, cache_dir: str = None):
        """
        初始化模型缓存管理器

        Args:
            cache_dir: 缓存目录路径
        """
        if cache_dir is None:
            # 默认缓存目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            cache_dir = os.path.join(project_root, 'cache', 'models')

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # HuggingFace 缓存环境变量
        os.environ['HF_HOME'] = str(self.cache_dir)
        os.environ['HUGGINGFACE_HUB_CACHE'] = str(self.cache_dir)

        log_info(f"模型缓存目录: {self.cache_dir}")

    def get_cached_models(self) -> List[str]:
        """
        获取已缓存的模型列表

        Returns:
            已缓存的模型ID列表
        """
        cached_models = []

        # 遍历缓存目录
        for item in self.cache_dir.iterdir():
            if item.is_dir() and item.name.startswith('models--'):
                # 从 models--author--ModelName 格式提取模型ID
                model_id = item.name.replace('models--', '').replace('--', '/')
                cached_models.append(model_id)

        return cached_models

    def is_model_cached(self, model_id: str) -> bool:
        """
        检查模型是否已缓存

        Args:
            model_id: 模型ID，如 'NeoQuasar/Kronos-small'

        Returns:
            模型是否已缓存
        """
        # 转换模型ID为目录名格式
        cache_name = f"models--{model_id.replace('/', '--')}"
        cache_path = self.cache_dir / cache_name

        # 检查是否存在
        if not cache_path.exists():
            return False

        # 检查是否有有效文件
        has_files = False
        for file in cache_path.rglob('*'):
            if file.is_file() and not file.name.endswith('.json'):
                has_files = True
                break

        return has_files

    def get_model_size(self, model_id: str) -> int:
        """
        获取模型缓存大小（字节）

        Args:
            model_id: 模型ID

        Returns:
            模型大小（字节）
        """
        cache_name = f"models--{model_id.replace('/', '--')}"
        cache_path = self.cache_dir / cache_name

        if not cache_path.exists():
            return 0

        total_size = 0
        for file in cache_path.rglob('*'):
            if file.is_file():
                total_size += file.stat().st_size

        return total_size

    def delete_model_cache(self, model_id: str) -> bool:
        """
        删除模型缓存

        Args:
            model_id: 模型ID

        Returns:
            是否成功删除
        """
        cache_name = f"models--{model_id.replace('/', '--')}"
        cache_path = self.cache_dir / cache_name

        if not cache_path.exists():
            log_info(f"模型缓存不存在: {model_id}")
            return False

        try:
            shutil.rmtree(cache_path)
            log_info(f"已删除模型缓存: {model_id}")
            return True
        except Exception as e:
            log_error(f"删除模型缓存失败: {e}")
            return False

    def clear_all_cache(self) -> bool:
        """
        清除所有模型缓存

        Returns:
            是否成功清除
        """
        try:
            # 删除所有 models-- 开头的目录
            for item in self.cache_dir.iterdir():
                if item.is_dir() and item.name.startswith('models--'):
                    shutil.rmtree(item)
                    log_info(f"已删除: {item.name}")

            return True
        except Exception as e:
            log_error(f"清除缓存失败: {e}")
            return False

    def get_cache_info(self) -> Dict[str, Any]:
        """
        获取缓存信息

        Returns:
            缓存信息字典
        """
        cached_models = self.get_cached_models()
        total_size = 0

        model_info = {}
        for model_id in cached_models:
            size = self.get_model_size(model_id)
            total_size += size
            model_info[model_id] = {
                'size_bytes': size,
                'size_mb': round(size / (1024 * 1024), 2),
                'path': str(self.cache_dir / f"models--{model_id.replace('/', '--')}")
            }

        return {
            'cache_dir': str(self.cache_dir),
            'total_models': len(cached_models),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'models': model_info
        }

    def load_model_from_cache(self, model_id: str, model_class, tokenizer_class=None):
        """
        从缓存加载模型

        Args:
            model_id: 模型ID
            model_class: 模型类
            tokenizer_class: tokenizer类（可选）

        Returns:
            模型实例或None
        """
        if not self.is_model_cached(model_id):
            log_info(f"模型未缓存: {model_id}")
            return None

        try:
            log_info(f"从缓存加载模型: {model_id}")
            model = model_class.from_pretrained(model_id)
            result = {'model': model}

            if tokenizer_class:
                tokenizer = tokenizer_class.from_pretrained(model_id)
                result['tokenizer'] = tokenizer

            return result

        except Exception as e:
            log_error(f"从缓存加载模型失败: {e}")
            return None

    def download_model(self, model_id: str, model_class, tokenizer_class=None):
        """
        下载模型到缓存

        Args:
            model_id: 模型ID
            model_class: 模型类
            tokenizer_class: tokenizer类（可选）

        Returns:
            模型实例或None
        """
        try:
            log_info(f"开始下载模型: {model_id}")

            model = model_class.from_pretrained(model_id)
            result = {'model': model}

            if tokenizer_class:
                tokenizer = tokenizer_class.from_pretrained(model_id)
                result['tokenizer'] = tokenizer

            log_info(f"模型下载完成: {model_id}")
            return result

        except Exception as e:
            log_error(f"模型下载失败: {e}")
            return None

    def get_or_download_model(
        self,
        model_id: str,
        model_class,
        tokenizer_class=None,
        force_download: bool = False
    ):
        """
        获取或下载模型

        Args:
            model_id: 模型ID
            model_class: 模型类
            tokenizer_class: tokenizer类（可选）
            force_download: 是否强制重新下载

        Returns:
            模型实例或None
        """
        if force_download:
            log_info(f"强制重新下载模型: {model_id}")
            return self.download_model(model_id, model_class, tokenizer_class)

        # 检查缓存
        if self.is_model_cached(model_id):
            log_info(f"使用缓存的模型: {model_id}")
            return self.load_model_from_cache(model_id, model_class, tokenizer_class)

        # 下载模型
        log_info(f"模型未缓存，开始下载: {model_id}")
        return self.download_model(model_id, model_class, tokenizer_class)


# 全局模型缓存实例
_cache_instance: Optional[ModelCache] = None


def get_model_cache() -> ModelCache:
    """
    获取全局模型缓存实例（单例模式）

    Returns:
        ModelCache 实例
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = ModelCache()
    return _cache_instance


def setup_model_cache(cache_dir: str = None) -> ModelCache:
    """
    设置全局模型缓存

    Args:
        cache_dir: 缓存目录路径

    Returns:
        ModelCache 实例
    """
    global _cache_instance
    _cache_instance = ModelCache(cache_dir)
    return _cache_instance
