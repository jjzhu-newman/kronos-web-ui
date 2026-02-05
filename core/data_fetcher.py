"""
增强版市场数据获取器
支持多数据源和自动降级策略

A股数据源优先级：
1. Akshare（主数据源，免费，无需注册）
2. Baostock（第一备用，免费，需简单注册）
3. Tushare（第二备用，需token，积分限制）
"""

import pandas as pd
import numpy as np
import requests
import datetime
import time
import os
from typing import Optional, Dict, Any, Tuple
import warnings

warnings.filterwarnings('ignore')

# 导入日志记录器
try:
    from .logger import get_logger
    logger = get_logger()
except:
    logger = None


def log_info(msg: str):
    """日志记录辅助函数"""
    if logger:
        logger.info(msg)
    else:
        print(f"[INFO] {msg}")


def log_warning(msg: str):
    """日志记录辅助函数"""
    if logger:
        logger.warning(msg)
    else:
        print(f"[WARNING] {msg}")


def log_error(msg: str):
    """日志记录辅助函数"""
    if logger:
        logger.error(msg)
    else:
        print(f"[ERROR] {msg}")


def log_exception(msg: str):
    """日志记录辅助函数"""
    if logger:
        logger.exception(msg)
    else:
        print(f"[EXCEPTION] {msg}")


class MarketDataFetcher:
    """
    统一市场数据获取器
    支持多数据源和自动降级
    """

    def __init__(self, tushare_token: str = None, baostock_token: str = None):
        """
        初始化数据获取器

        Args:
            tushare_token: Tushare API token
            baostock_token: Baostock token (暂时不需要)
        """
        self.supported_sources = [
            'binance', 'binance_futures', 'yahoo',
            'akshare', 'baostock', 'tushare', 'local'
        ]
        self.binance_base_url = "https://api.binance.com"

        # Tushare 配置
        self.tushare_token = tushare_token or os.getenv('TUSHARE_TOKEN')
        self.ts = None
        if self.tushare_token:
            try:
                import tushare as ts
                ts.set_token(self.tushare_token)
                self.ts = ts.pro_api()
                log_info("Tushare 初始化成功")
            except ImportError:
                log_warning("Tushare 未安装")
            except Exception as e:
                log_warning(f"Tushare 初始化失败: {e}")

        # Baostock 配置
        self.bs = None
        try:
            import baostock as bs
            self.bs = bs
            # 登录 Baostock
            lg = bs.login()
            if lg.error_code == '0':
                log_info("Baostock 登录成功")
            else:
                log_warning(f"Baostock 登录失败: {lg.error_msg}")
                self.bs = None
        except ImportError:
            log_warning("Baostock 未安装，请运行: pip install baostock")
        except Exception as e:
            log_warning(f"Baostock 初始化失败: {e}")

        # Akshare 检查
        try:
            import akshare as ak
            self.ak_available = True
            log_info("Akshare 可用")
        except ImportError:
            self.ak_available = False
            log_warning("Akshare 未安装，请运行: pip install akshare")

    def fetch_a_stock_with_fallback(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        adjust: str = 'qfq'
    ) -> pd.DataFrame:
        """
        A股数据获取 - 支持自动降级

        优先级: Akshare → Baostock → Tushare

        Args:
            symbol: 股票代码（如 '601212', '000001'）
            start_date: 开始日期 (YYYYMMDD 格式)
            end_date: 结束日期 (YYYYMMDD 格式)
            adjust: 复权类型 ('qfq'=前复权, 'hfq'=后复权, ''=不复权)

        Returns:
            DataFrame with columns: timestamps, open, high, low, close, volume, amount
        """
        # 1. 尝试 Akshare（主数据源）
        if self.ak_available:
            try:
                log_info(f"尝试使用 Akshare 获取 {symbol} 数据...")
                df = self.fetch_akshare(symbol, start_date, end_date, adjust)
                log_info(f"Akshare 成功获取 {len(df)} 条数据")
                return df
            except Exception as e:
                log_warning(f"Akshare 获取 {symbol} 失败: {e}")

        # 2. 尝试 Baostock（第一备用）
        if self.bs is not None:
            try:
                log_info(f"尝试使用 Baostock 获取 {symbol} 数据...")
                df = self.fetch_baostock(symbol, start_date, end_date)
                log_info(f"Baostock 成功获取 {len(df)} 条数据")
                return df
            except Exception as e:
                log_warning(f"Baostock 获取 {symbol} 失败: {e}")

        # 3. 尝试 Tushare（第二备用）
        if self.ts is not None:
            try:
                log_info(f"尝试使用 Tushare 获取 {symbol} 数据...")
                df = self.fetch_tushare(symbol, start_date, end_date)
                log_info(f"Tushare 成功获取 {len(df)} 条数据")
                return df
            except Exception as e:
                log_warning(f"Tushare 获取 {symbol} 失败: {e}")

        # 所有数据源均失败
        raise ValueError(
            f"所有数据源均无法获取 {symbol} 的数据。\n"
            f"请确保已安装数据源库: pip install akshare baostock akshare"
        )

    def fetch_baostock(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        frequency: str = "d"
    ) -> pd.DataFrame:
        """
        从 Baostock 获取A股数据

        Args:
            symbol: 股票代码（如 'sh.601212', 'sz.000001' 或 '601212', '000001'）
            start_date: 开始日期 (YYYY-MM-DD 格式)
            end_date: 结束日期 (YYYY-MM-DD 格式)
            frequency: 数据频率 (d=日线, w=周线, m=月线)

        Returns:
            DataFrame with K-line data
        """
        if self.bs is None:
            raise ValueError("Baostock 未初始化，请先安装 baostock: pip install baostock")

        # 默认日期范围：最近2年
        if end_date is None:
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        if start_date is None:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=730)).strftime('%Y-%m-%d')

        # 标准化股票代码格式
        symbol = symbol.upper()
        if not symbol.startswith(('SH.', 'SZ.')):
            # 判断是上海还是深圳
            if symbol.startswith('6') or symbol.startswith('5'):
                symbol = f'SH.{symbol}'
            elif symbol.startswith('0') or symbol.startswith('3'):
                symbol = f'SZ.{symbol}'
            else:
                raise ValueError(f"无法识别的股票代码: {symbol}")

        # 转换日期格式为 Baostock 格式
        start_date = start_date.replace('-', '')
        end_date = end_date.replace('-', '')

        # 获取数据
        rs = self.bs.query_history_k_data_plus(
            symbol,
            "date,open,high,low,close,volume,amount",
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag="2"  # 2=前复权
        )

        if rs.error_code != '0':
            raise ValueError(f"Baostock API 错误: {rs.error_msg}")

        # 转换为 DataFrame
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())

        if not data_list:
            raise ValueError(f"Baostock 未获取到 {symbol} 的数据")

        df = pd.DataFrame(data_list, columns=rs.fields)

        # 重命名列
        column_map = {
            'date': 'timestamps',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'amount': 'amount'
        }
        df.rename(columns=column_map, inplace=True)

        # 数据类型转换
        for col in ['open', 'high', 'low', 'close', 'volume', 'amount']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['timestamps'] = pd.to_datetime(df['timestamps'])

        # 删除NaN行并排序
        df = df.dropna()
        df = df.sort_values('timestamps').reset_index(drop=True)

        return df

    def fetch_akshare(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        adjust: str = 'qfq'
    ) -> pd.DataFrame:
        """
        从 Akshare 获取A股数据

        Args:
            symbol: 股票代码（不带交易所后缀，如 '601212', '000001'）
            start_date: 开始日期 (YYYYMMDD 格式)
            end_date: 结束日期 (YYYYMMDD 格式)
            adjust: 复权类型 ('qfq'=前复权, 'hfq'=后复权, ''=不复权)

        Returns:
            DataFrame with K-line data
        """
        try:
            import akshare as ak
        except ImportError:
            raise ValueError("Akshare 未安装，请运行: pip install akshare")

        # 默认日期范围
        if end_date is None:
            end_date = datetime.datetime.now().strftime('%Y%m%d')
        if start_date is None:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=730)).strftime('%Y%m%d')

        # 转换复权参数
        ak_adjust = "qfq" if adjust == 'qfq' else ("hfq" if adjust == 'hfq' else "")

        # 获取数据 - 使用 stock_zh_a_hist 方法
        try:
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date.replace('-', ''),
                end_date=end_date.replace('-', ''),
                adjust=ak_adjust
            )
        except Exception as e:
            # 尝试备用方法
            try:
                df = ak.stock_zh_a_daily(
                    symbol=f"sh{symbol}" if symbol.startswith('6') else f"sz{symbol}",
                    start_date=start_date,
                    adjust=ak_adjust
                )
            except Exception as e2:
                raise ValueError(f"Akshare 获取数据失败: {e}, 备用方法也失败: {e2}")

        if df.empty:
            raise ValueError(f"Akshare 未获取到 {symbol} 的数据")

        # 重命名列（Akshare 返回中文列名）
        column_map = {
            '日期': 'timestamps',
            '开盘': 'open',
            '最高': 'high',
            '最低': 'low',
            '收盘': 'close',
            '成交量': 'volume',
            '成交额': 'amount'
        }
        df.rename(columns={k: v for k, v in column_map.items() if k in df.columns}, inplace=True)

        # 如果列名是英文，使用英文映射
        if 'timestamps' not in df.columns:
            column_map_en = {
                'date': 'timestamps',
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'volume': 'volume',
                'amount': 'amount'
            }
            df.rename(columns={k: v for k, v in column_map_en.items() if k in df.columns}, inplace=True)

        # 数据类型转换
        for col in ['open', 'high', 'low', 'close', 'volume', 'amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        df['timestamps'] = pd.to_datetime(df['timestamps'])

        # 添加amount列（如果不存在）
        if 'amount' not in df.columns or df['amount'].isnull().all():
            df['amount'] = df['volume'] * df[['open', 'high', 'low', 'close']].mean(axis=1)

        # 选择需要的列
        required_cols = ['timestamps', 'open', 'high', 'low', 'close', 'volume', 'amount']
        df = df[[c for c in required_cols if c in df.columns]]

        # 删除NaN行并排序
        df = df.dropna()
        df = df.sort_values('timestamps').reset_index(drop=True)

        return df

    def fetch_tushare(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        从 Tushare 获取A股数据

        Args:
            symbol: 股票代码（如 '601212.SH', '000001.SZ' 或 '601212', '000001'）
            start_date: 开始日期 (YYYYMMDD 格式)
            end_date: 结束日期 (YYYYMMDD 格式)

        Returns:
            DataFrame with K-line data
        """
        if self.ts is None:
            raise ValueError("Tushare 未配置，请设置 token 或从环境变量 TUSHARE_TOKEN 读取")

        # 默认日期范围
        if end_date is None:
            end_date = datetime.datetime.now().strftime('%Y%m%d')
        if start_date is None:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=730)).strftime('%Y%m%d')

        # 标准化股票代码格式
        if '.' not in symbol:
            # 判断是上海还是深圳
            if symbol.startswith('6') or symbol.startswith('5'):
                symbol = f'{symbol}.SH'
            elif symbol.startswith('0') or symbol.startswith('3'):
                symbol = f'{symbol}.SZ'

        # 获取数据
        df = self.ts.daily(
            ts_code=symbol,
            start_date=start_date,
            end_date=end_date
        )

        if df.empty:
            raise ValueError(f"Tushare 未获取到 {symbol} 的数据")

        # 重命名列
        column_map = {
            'trade_date': 'timestamps',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'vol': 'volume',
            'amount': 'amount'
        }
        df.rename(columns=column_map, inplace=True)

        # 数据类型转换
        for col in ['open', 'high', 'low', 'close', 'volume', 'amount']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['timestamps'] = pd.to_datetime(df['timestamps'], format='%Y%m%d')

        # 选择需要的列
        df = df[['timestamps', 'open', 'high', 'low', 'close', 'volume', 'amount']]

        # 删除NaN行并排序
        df = df.dropna()
        df = df.sort_values('timestamps').reset_index(drop=True)

        return df

    def fetch_binance(
        self,
        symbol: str,
        interval: str = '1h',
        limit: int = 500,
        end_time: Optional[int] = None
    ) -> pd.DataFrame:
        """从 Binance 获取加密货币数据"""
        try:
            url = f"{self.binance_base_url}/api/v3/klines"
            params = {
                'symbol': symbol.upper(),
                'interval': interval,
                'limit': min(limit, 1000)
            }
            if end_time:
                params['endTime'] = end_time

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                raise ValueError(f"Binance 未返回 {symbol} 的数据")

            df = pd.DataFrame(data, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ])

            df['timestamps'] = pd.to_datetime(df['open_time'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)

            df = df[['timestamps', 'open', 'high', 'low', 'close', 'volume']].copy()
            df['amount'] = df['volume'] * df[['open', 'high', 'low', 'close']].mean(axis=1)

            return df

        except Exception as e:
            raise ValueError(f"Binance 数据获取失败: {str(e)}")

    def fetch_yahoo(
        self,
        symbol: str,
        period: str = '3mo',
        interval: str = '1h'
    ) -> pd.DataFrame:
        """从 Yahoo Finance 获取数据"""
        try:
            import yfinance as yf
        except ImportError:
            raise ValueError("yfinance 未安装，请运行: pip install yfinance")

        try:
            ticker = yf.Ticker(symbol.upper())
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                raise ValueError(f"Yahoo Finance 未返回 {symbol} 的数据")

            df = df.reset_index()

            # 重命名列
            if 'Date' in df.columns:
                df.rename(columns={'Date': 'timestamps'}, inplace=True)
            elif 'Datetime' in df.columns:
                df.rename(columns={'Datetime': 'timestamps'}, inplace=True)

            column_map = {
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            }
            df.rename(columns=column_map, inplace=True)

            df['timestamps'] = pd.to_datetime(df['timestamps'])
            df = df[['timestamps', 'open', 'high', 'low', 'close', 'volume']].copy()
            df['amount'] = df['volume'] * df[['open', 'high', 'low', 'close']].mean(axis=1)

            return df.dropna()

        except Exception as e:
            raise ValueError(f"Yahoo Finance 数据获取失败: {str(e)}")

    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """验证数据格式"""
        required_cols = ['open', 'high', 'low', 'close']

        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"缺少必需列: {missing_cols}"

        if not all(pd.api.types.is_numeric_dtype(df[col]) for col in required_cols):
            return False, "价格列必须为数值类型"

        if df[required_cols].isnull().any().any():
            return False, "数据包含 NaN 值"

        if len(df) < 10:
            return False, f"数据量不足: {len(df)} 行，至少需要 10 行"

        if 'timestamps' not in df.columns:
            return False, "缺少 timestamps 列"

        return True, ""
