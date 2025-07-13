"""
Configuration management for the stock prediction prototype.
"""
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pathlib import Path

# Load environment variables
load_dotenv()

class DatabaseConfig(BaseModel):
    url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/stock_prediction"))
    
class RedisConfig(BaseModel):
    url: str = Field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379"))

class APIConfig(BaseModel):
    host: str = Field(default_factory=lambda: os.getenv("API_HOST", "0.0.0.0"))
    port: int = Field(default_factory=lambda: int(os.getenv("API_PORT", "8000")))
    reload: bool = Field(default_factory=lambda: os.getenv("API_RELOAD", "true").lower() == "true")

class MarketStackConfig(BaseModel):
    api_key: str = Field(default_factory=lambda: os.getenv("MARKETSTACK_API_KEY", "102b76768338d536bf46fb894114cf29"))
    base_url: str = Field(default_factory=lambda: os.getenv("MARKETSTACK_BASE_URL", "http://api.marketstack.com/v1"))

class ModelConfig(BaseModel):
    cache_duration: int = Field(default_factory=lambda: int(os.getenv("MODEL_CACHE_DURATION", "86400")))
    retrain_interval: int = Field(default_factory=lambda: int(os.getenv("RETRAIN_INTERVAL", "604800")))
    confidence_threshold: float = Field(default_factory=lambda: float(os.getenv("PREDICTION_CONFIDENCE_THRESHOLD", "0.6")))

class AnalysisConfig(BaseModel):
    technical_indicators_enabled: bool = Field(default_factory=lambda: os.getenv("TECHNICAL_INDICATORS_ENABLED", "true").lower() == "true")
    fundamental_analysis_enabled: bool = Field(default_factory=lambda: os.getenv("FUNDAMENTAL_ANALYSIS_ENABLED", "true").lower() == "true")
    sentiment_analysis_enabled: bool = Field(default_factory=lambda: os.getenv("SENTIMENT_ANALYSIS_ENABLED", "true").lower() == "true")
    news_lookback_days: int = Field(default_factory=lambda: int(os.getenv("NEWS_LOOKBACK_DAYS", "30")))

class ReportConfig(BaseModel):
    cache_duration: int = Field(default_factory=lambda: int(os.getenv("REPORT_CACHE_DURATION", "3600")))
    pdf_generation_enabled: bool = Field(default_factory=lambda: os.getenv("PDF_GENERATION_ENABLED", "true").lower() == "true")

class RiskManagementConfig(BaseModel):
    max_risk_score: int = Field(default_factory=lambda: int(os.getenv("MAX_RISK_SCORE", "80")))
    min_confidence_for_buy: float = Field(default_factory=lambda: float(os.getenv("MIN_CONFIDENCE_FOR_BUY", "0.7")))
    min_confidence_for_sell: float = Field(default_factory=lambda: float(os.getenv("MIN_CONFIDENCE_FOR_SELL", "0.7")))

class LoggingConfig(BaseModel):
    level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    file: str = Field(default_factory=lambda: os.getenv("LOG_FILE", "logs/app.log"))

class Settings(BaseModel):
    """Main application settings"""
    project_name: str = "Stock Prediction Prototype"
    version: str = "0.1.0"
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    
    # Component configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    marketstack: MarketStackConfig = Field(default_factory=MarketStackConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    report: ReportConfig = Field(default_factory=ReportConfig)
    risk_management: RiskManagementConfig = Field(default_factory=RiskManagementConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()

def load_config_from_file(config_path: str = "config/settings.json") -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config file {config_path}: {e}")
    return {}

def get_settings() -> Settings:
    """Get application settings"""
    return settings
