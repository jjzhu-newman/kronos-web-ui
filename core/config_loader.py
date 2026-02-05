"""
配置加载器模块
负责加载和管理应用配置
"""

import os
import json
from typing import Dict, Any


class ConfigLoader:
    """配置加载器类"""

    def __init__(self, config_dir: str = None):
        """
        初始化配置加载器

        Args:
            config_dir: 配置文件目录，默认为 ../config
        """
        if config_dir is None:
            # 默认配置目录为项目根目录下的 config 文件夹
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.join(os.path.dirname(current_dir), 'config')

        self.config_dir = config_dir
        self.config = {}
        self.models_config = {}

        self._load_configs()

    def _load_configs(self):
        """加载所有配置文件"""
        # 加载主配置文件
        config_path = os.path.join(self.config_dir, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        # 加载模型配置文件
        models_config_path = os.path.join(self.config_dir, 'models.json')
        if os.path.exists(models_config_path):
            with open(models_config_path, 'r', encoding='utf-8') as f:
                self.models_config = json.load(f)
        else:
            raise FileNotFoundError(f"模型配置文件不存在: {models_config_path}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值，支持点号分隔的嵌套键

        Args:
            key: 配置键，支持 'app.port' 这样的嵌套格式
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_model_config(self, model_key: str) -> Dict[str, Any]:
        """
        获取特定模型的配置

        Args:
            model_key: 模型键，如 'kronos-small'

        Returns:
            模型配置字典
        """
        return self.models_config.get('available_models', {}).get(model_key, {})

    def get_all_models(self) -> Dict[str, Any]:
        """获取所有可用模型配置"""
        return self.models_config.get('available_models', {})

    def get_data_source_config(self, market: str = 'a_stocks') -> Dict[str, Any]:
        """
        获取数据源配置

        Args:
            market: 市场类型，如 'a_stocks', 'crypto', 'global_stocks'

        Returns:
            数据源配置字典
        """
        return self.config.get('data_sources', {}).get(market, {})

    def get_cache_dir(self) -> str:
        """获取缓存目录路径"""
        cache_dir = self.config.get('paths', {}).get('cache_dir', 'cache/models')
        # 转换为绝对路径
        if not os.path.isabs(cache_dir):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cache_dir = os.path.join(project_root, cache_dir)
        return cache_dir

    def get_log_dir(self) -> str:
        """获取日志目录路径"""
        log_dir = self.config.get('paths', {}).get('log_dir', 'logs')
        if not os.path.isabs(log_dir):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_dir = os.path.join(project_root, log_dir)
        return log_dir

    def get_export_dir(self) -> str:
        """获取导出目录路径"""
        export_dir = self.config.get('paths', {}).get('export_dir', 'static/exports')
        if not os.path.isabs(export_dir):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            export_dir = os.path.join(project_root, export_dir)
        return export_dir

    def reload(self):
        """重新加载配置文件"""
        self._load_configs()


# 全局配置实例
_config_instance = None


def get_config() -> ConfigLoader:
    """
    获取全局配置实例（单例模式）

    Returns:
        ConfigLoader实例
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance
