"""
Kronos Web UI - Enhanced Backend
一键式金融预测平台
"""

import os
import sys

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# 添加路径：优先使用 core 目录
sys.path.insert(0, current_dir)
sys.path.insert(0, project_root)

import pandas as pd
import numpy as np
import json
import datetime
import warnings

warnings.filterwarnings('ignore')

# Fix Windows console encoding (if on Windows)
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass

# 设置 HuggingFace 缓存目录到项目本地
cache_dir = os.path.join(project_root, 'cache', 'models')
os.makedirs(cache_dir, exist_ok=True)
os.environ['HF_HOME'] = cache_dir
os.environ['HUGGINGFACE_HUB_CACHE'] = cache_dir

# 导入核心模块
from core.config_loader import get_config
from core.logger import setup_logger, get_logger
from core.data_fetcher import MarketDataFetcher
from core.model_cache import get_model_cache

# 导入模型
try:
    from core.model import Kronos, KronosTokenizer, KronosPredictor
    MODEL_AVAILABLE = True
except ImportError as e:
    MODEL_AVAILABLE = False
    print(f"Warning: Kronos model not available: {e}")

# Flask
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider

# Custom JSON provider for numpy types (Flask 3.x)
class NumpyJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return super().default(obj)


# Initialize
config = get_config()

# Setup logger
log_dir = config.get_log_dir()
os.makedirs(log_dir, exist_ok=True)
logger = setup_logger(
    name="KronosUI",
    log_dir=log_dir,
    level=config.get('logging.level', 'INFO'),
    console=config.get('logging.console', True),
    file=config.get('logging.file', True)
)

logger.info("Kronos UI 启动中...")

# Initialize Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(project_root, 'static'),
    template_folder=os.path.join(project_root, 'templates')
)
app.json = NumpyJSONProvider(app)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# Global state
fetcher = None
predictor = None
model_config = None
model_cache = get_model_cache()

# Available models from config
AVAILABLE_MODELS = config.get_all_models()

# Popular symbols
POPULAR_SYMBOLS = {
    'crypto': [
        {'symbol': 'BTCUSDT', 'name': 'Bitcoin', 'icon': '₿'},
        {'symbol': 'ETHUSDT', 'name': 'Ethereum', 'icon': 'Ξ'},
        {'symbol': 'BNBUSDT', 'name': 'BNB', 'icon': '◆'},
        {'symbol': 'SOLUSDT', 'name': 'Solana', 'icon': '◎'},
    ],
    'a_stocks': [
        {'symbol': '601212', 'name': '白银有色', 'icon': ''},
        {'symbol': '600519', 'name': '贵州茅台', 'icon': ''},
        {'symbol': '600036', 'name': '招商银行', 'icon': ''},
        {'symbol': '601318', 'name': '中国平安', 'icon': ''},
        {'symbol': '600276', 'name': '恒瑞医药', 'icon': ''},
    ],
    'stocks': [
        {'symbol': 'AAPL', 'name': 'Apple', 'icon': ''},
        {'symbol': 'GOOGL', 'name': 'Google', 'icon': ''},
        {'symbol': 'MSFT', 'name': 'Microsoft', 'icon': ''},
        {'symbol': 'TSLA', 'name': 'Tesla', 'icon': ''},
    ],
}


@app.route('/')
def index():
    """Render main application page"""
    return render_template('index.html')


@app.route('/api/status')
def status():
    """Get system status"""
    global fetcher
    if fetcher is None:
        fetcher = MarketDataFetcher()

    # Check CUDA availability
    cuda_available = False
    try:
        import torch
        cuda_available = torch.cuda.is_available()
    except:
        pass

    # Get cache info
    cache_info = model_cache.get_cache_info()

    return jsonify({
        'model_available': MODEL_AVAILABLE,
        'model_loaded': predictor is not None,
        'model_info': {
            'name': model_config['name'] if model_config else None,
            'params': model_config['params'] if model_config else None
        } if model_config else None,
        'cache_info': cache_info,
        'cuda_available': cuda_available,
        'version': config.get('app.version', '2.0.0')
    })


@app.route('/api/models')
def get_models():
    """Get available models"""
    # Add cached status for both model and tokenizer
    models_info = []
    for key, model in AVAILABLE_MODELS.items():
        model_info = model.copy()
        model_info['key'] = key

        # Check if both model and tokenizer are cached
        model_cached = model_cache.is_model_cached(model['model_id'])
        tokenizer_cached = model_cache.is_model_cached(model['tokenizer_id'])

        # Model is considered cached if both are cached
        model_info['cached'] = model_cached and tokenizer_cached
        model_info['model_cached'] = model_cached
        model_info['tokenizer_cached'] = tokenizer_cached

        models_info.append(model_info)

    # Check CUDA availability
    cuda_available = False
    try:
        import torch
        cuda_available = torch.cuda.is_available()
    except:
        pass

    return jsonify({
        'models': models_info,
        'model_available': MODEL_AVAILABLE,
        'cuda_available': cuda_available
    })


@app.route('/api/load-model', methods=['POST'])
def load_model():
    """Load Kronos model"""
    global predictor, model_config

    if not MODEL_AVAILABLE:
        return jsonify({'error': 'Kronos model not available'}), 400

    try:
        data = request.get_json()
        model_key = data.get('model_key', 'kronos-small')
        device = data.get('device', 'cpu')
        force_download = data.get('force_download', False)

        if model_key not in AVAILABLE_MODELS:
            return jsonify({'error': f'Unknown model: {model_key}'}), 400

        model_cfg = AVAILABLE_MODELS[model_key]

        # Validate device availability
        import torch
        cuda_available = torch.cuda.is_available()
        mps_available = hasattr(torch.backends, 'mps') and torch.backends.mps.is_available()

        # Auto-downgrade to CPU if requested device is not available
        if device.startswith('cuda') and not cuda_available:
            logger.warning(f"CUDA requested but not available, downgrading to CPU")
            device = 'cpu'
        elif device == 'mps' and not mps_available:
            logger.warning(f"MPS requested but not available, downgrading to CPU")
            device = 'cpu'

        logger.info(f"加载模型: {model_cfg['name']} on {device}")

        # Get cache directory
        cache_dir = os.path.join(project_root, 'cache', 'models')

        # Load tokenizer separately
        try:
            logger.info(f"加载 tokenizer: {model_cfg['tokenizer_id']}")
            tokenizer = KronosTokenizer.from_pretrained(
                model_cfg['tokenizer_id'],
                cache_dir=cache_dir,
                local_files_only=False
            )
        except Exception as e:
            logger.exception(f"Tokenizer 加载失败: {e}")
            return jsonify({'error': f'Failed to load tokenizer: {str(e)}'}), 500

        # Load model
        try:
            logger.info(f"加载模型: {model_cfg['model_id']}")
            model = Kronos.from_pretrained(
                model_cfg['model_id'],
                cache_dir=cache_dir,
                local_files_only=False
            )
        except Exception as e:
            logger.exception(f"Model 加载失败: {e}")
            return jsonify({'error': f'Failed to load model: {str(e)}'}), 500

        # Create predictor
        predictor = KronosPredictor(
            model, tokenizer,
            device=device,
            max_context=model_cfg['context_length']
        )
        model_config = model_cfg

        logger.info(f"模型加载成功: {model_cfg['name']}")

        return jsonify({
            'success': True,
            'message': f'Loaded {model_cfg["name"]} ({model_cfg["params"]}) on {device}',
            'model': {
                'name': model_cfg['name'],
                'params': model_cfg['params'],
                'context_length': model_cfg['context_length']
            }
        })

    except Exception as e:
        logger.exception(f"模型加载失败: {e}")
        return jsonify({'error': f'Failed to load model: {str(e)}'}), 500


@app.route('/api/cache-info')
def cache_info():
    """Get model cache information"""
    return jsonify(model_cache.get_cache_info())


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear model cache"""
    try:
        data = request.get_json()
        model_id = data.get('model_id')

        if model_id:
            success = model_cache.delete_model_cache(model_id)
            message = f'Cache cleared for {model_id}'
        else:
            success = model_cache.clear_all_cache()
            message = 'All cache cleared'

        return jsonify({
            'success': success,
            'message': message
        })

    except Exception as e:
        logger.error(f"清除缓存失败: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/symbols')
def get_symbols():
    """Get popular trading symbols"""
    category = request.args.get('category', 'crypto')

    if category in POPULAR_SYMBOLS:
        return jsonify({'symbols': POPULAR_SYMBOLS[category]})

    return jsonify({'symbols': []})


@app.route('/api/fetch-data', methods=['POST'])
def fetch_data():
    """Fetch market data"""
    global fetcher

    try:
        if fetcher is None:
            fetcher = MarketDataFetcher()

        data = request.get_json()
        source = data.get('source', 'binance')
        symbol = data.get('symbol', 'BTCUSDT')
        interval = data.get('interval', '1h')
        limit = data.get('limit', 500)

        # Fetch data based on source
        if source == 'binance':
            df = fetcher.fetch_binance(symbol, interval, limit)
        elif source == 'binance_futures':
            df = fetcher.fetch_binance_futures(symbol, interval, limit)
        elif source == 'yahoo':
            df = fetcher.fetch_yahoo(symbol, period='3mo', interval=interval)
        elif source == 'akshare':
            df = fetcher.fetch_a_stock_with_fallback(symbol)
        elif source == 'baostock':
            df = fetcher.fetch_baostock(symbol)
        elif source == 'tushare':
            df = fetcher.fetch_tushare(symbol)
        elif source == 'local':
            df = fetcher.fetch_local_file(symbol)
        else:
            return jsonify({'error': f'Unknown source: {source}'}), 400

        # Validate data
        is_valid, error_msg = fetcher.validate_data(df)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Return data info
        return jsonify({
            'success': True,
            'data_info': {
                'rows': len(df),
                'start_date': df['timestamps'].iloc[0].isoformat(),
                'end_date': df['timestamps'].iloc[-1].isoformat(),
                'interval': interval,
                'price_range': {
                    'min': float(df['close'].min()),
                    'max': float(df['close'].max()),
                    'latest': float(df['close'].iloc[-1])
                },
                'has_volume': 'volume' in df.columns
            },
            'sample_data': df.tail(10).to_dict('records')
        })

    except Exception as e:
        logger.exception(f"数据获取失败: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/quick-predict', methods=['POST'])
def quick_predict():
    """One-click fetch and predict"""
    global predictor, fetcher

    if predictor is None:
        return jsonify({'error': 'Model not loaded. Please load a model first.'}), 400

    if fetcher is None:
        fetcher = MarketDataFetcher()

    try:
        data = request.get_json()
        source = data.get('source', 'binance')
        symbol = data.get('symbol', 'BTCUSDT')
        interval = data.get('interval', '1h')
        lookback = int(data.get('lookback', 400))
        pred_len = int(data.get('pred_len', 120))
        temperature = float(data.get('temperature', 1.0))
        top_p = float(data.get('top_p', 0.9))
        sample_count = int(data.get('sample_count', 1))

        logger.info(f"开始预测: {symbol} ({source}), lookback={lookback}, pred_len={pred_len}")

        # Fetch data (use fallback for A-stocks)
        if source in ['akshare', 'baostock', 'tushare']:
            df = fetcher.fetch_a_stock_with_fallback(symbol)
        elif source == 'binance':
            df = fetcher.fetch_binance(symbol, interval, limit=max(lookback + pred_len + 50, 600))
        elif source == 'yahoo':
            df = fetcher.fetch_yahoo(symbol, period='3mo', interval=interval)
        else:
            return jsonify({'error': f'Unknown source: {source}'}), 400

        # Prepare inputs
        if len(df) < lookback:
            return jsonify({'error': f'Insufficient data: got {len(df)} points, need {lookback}'}), 400

        x_df = df.iloc[-lookback:][['open', 'high', 'low', 'close', 'volume', 'amount']]
        x_timestamp = df.iloc[-lookback:]['timestamps']

        # Calculate future timestamps
        last_timestamp = df['timestamps'].iloc[-1]
        time_diffs = df['timestamps'].diff().dropna()
        time_diff = time_diffs.mode()[0] if len(time_diffs) > 0 else pd.Timedelta(hours=1)

        y_timestamp = pd.date_range(
            start=last_timestamp + time_diff,
            periods=pred_len,
            freq=time_diff
        )

        # Make prediction
        pred_df = predictor.predict(
            df=x_df,
            x_timestamp=x_timestamp,
            y_timestamp=y_timestamp,
            pred_len=pred_len,
            T=temperature,
            top_p=top_p,
            sample_count=sample_count
        )

        # Build response
        chart_data = {
            'historical': [
                {
                    'timestamp': row['timestamps'].isoformat() if pd.notna(row['timestamps']) else None,
                    'open': float(row['open']),
                    'high': float(row['high']),
                    'low': float(row['low']),
                    'close': float(row['close']),
                    'volume': float(row.get('volume', 0))
                }
                for _, row in df.iloc[-lookback:].iterrows()
            ],
            'prediction': [
                {
                    'timestamp': idx.isoformat() if hasattr(idx, 'isoformat') else str(idx),
                    'open': float(row['open']),
                    'high': float(row['high']),
                    'low': float(row['low']),
                    'close': float(row['close']),
                    'volume': float(row.get('volume', 0))
                }
                for idx, row in pred_df.iterrows()
            ]
        }

        # Calculate prediction statistics
        last_close = float(df['close'].iloc[-1])
        pred_closes = pred_df['close'].values
        pred_change = ((pred_closes[-1] - last_close) / last_close) * 100

        logger.info(f"预测完成: {symbol}, 预测涨跌: {pred_change:.2f}%")

        return jsonify({
            'success': True,
            'chart_data': chart_data,
            'metadata': {
                'symbol': symbol,
                'source': source,
                'interval': interval,
                'lookback': lookback,
                'pred_len': pred_len,
                'fetch_time': datetime.datetime.now().isoformat(),
                'model': model_config['name'] if model_config else None
            },
            'prediction_stats': {
                'last_price': last_close,
                'pred_start': float(pred_closes[0]),
                'pred_end': float(pred_closes[-1]),
                'change_percent': pred_change,
                'direction': 'up' if pred_change > 0 else 'down'
            }
        })

    except Exception as e:
        logger.exception(f"预测失败: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export-prediction', methods=['POST'])
def export_prediction():
    """Export prediction results to CSV/JSON"""
    try:
        data = request.get_json()
        chart_data = data.get('chart_data', {})
        metadata = data.get('metadata', {})
        format_type = data.get('format', 'csv')

        # Combine all data
        all_data = []
        for item in chart_data.get('historical', []):
            all_data.append({**item, 'type': 'historical'})
        for item in chart_data.get('prediction', []):
            all_data.append({**item, 'type': 'prediction'})

        df = pd.DataFrame(all_data)

        # Create export directory
        export_dir = config.get_export_dir()
        os.makedirs(export_dir, exist_ok=True)

        # Generate filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        symbol = metadata.get('symbol', 'unknown').replace('/', '_')

        if format_type == 'csv':
            filename = f'{symbol}_prediction_{timestamp}.csv'
            filepath = os.path.join(export_dir, filename)
            df.to_csv(filepath, index=False)
        else:
            filename = f'{symbol}_prediction_{timestamp}.json'
            filepath = os.path.join(export_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': metadata,
                    'data': all_data
                }, f, indent=2, ensure_ascii=False)

        logger.info(f"导出预测结果: {filename}")

        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/api/download/{filename}'
        })

    except Exception as e:
        logger.exception(f"导出失败: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download exported file"""
    export_dir = config.get_export_dir()
    return send_from_directory(export_dir, filename, as_attachment=True)


def main():
    """Main entry point"""
    port = config.get('app.port', 7070)
    host = config.get('app.host', '0.0.0.0')
    debug = config.get('app.debug', False)

    logger.info(f"Starting Kronos UI on http://{host}:{port}")
    logger.info(f"Model available: {MODEL_AVAILABLE}")

    print("=" * 60)
    print("Kronos Web UI - AI Financial Prediction Platform")
    print("=" * 60)
    print(f"Model Available: {MODEL_AVAILABLE}")
    print(f"Open browser: http://localhost:{port}")
    print("=" * 60)

    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    main()
