"""
Configuration management for Autonomous Trading Ecosystem.
Centralizes all configuration with environment-aware defaults.
Architectural Choice: Pydantic for runtime type validation and 
environment variable parsing, preventing configuration errors.
"""

import os
from typing import Dict, List, Optional, Union
from pydantic import BaseSettings, Field, validator
from enum import Enum

class TradingMode(str, Enum):
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"

class ExchangeType(str, Enum):
    BINANCE = "binance"
    COINBASE = "coinbase"
    KRAKEN = "kraken"
    ALPACA = "alpaca"  # For traditional markets

class ModelType(str, Enum):
    LSTM = "lstm"
    TRANSFORMER = "transformer"
    ENSEMBLE = "ensemble"

class Settings(BaseSettings):
    """Main application settings with validation"""
    
    # Application
    APP_NAME: str = "autonomous_trading_ecosystem"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Trading
    TRADING_MODE: TradingMode = Field(default=TradingMode.PAPER)
    DEFAULT_EXCHANGE: ExchangeType = Field(default=ExchangeType.BINANCE)
    SYMBOLS: List[str] = Field(default=["BTC/USDT", "ETH/USDT", "AAPL/USD"])
    TIMEFRAMES: List[str] = Field(default=["1h", "4h", "1d"])
    
    # Model Configuration
    PRIMARY_MODEL: ModelType = Field(default=ModelType.LSTM)
    TRAIN_EPOCHS: int = Field(default=100, ge=1, le=1000)
    BATCH_SIZE: int = Field(default=32, ge=8, le=256)
    LOOKBACK_WINDOW: int = Field(default=100, ge=10, le=500)
    
    # Risk Management
    MAX_POSITION_SIZE: float = Field(default=0.1, ge=0.01, le=1.0)  # 10% of portfolio
    STOP_LOSS_PCT: float = Field(default=0.02, ge=0.005, le=0.1)  # 2%
    MAX_DAILY_LOSS: float = Field(default=0.05, ge=0.01, le=0.2)  # 5%
    
    # Firebase Configuration (CRITICAL for state management)
    FIREBASE_PROJECT_ID: Optional[str] = Field(env="FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY: Optional[str] = Field(env="FIREBASE_PRIVATE_KEY")
    FIREBASE_CLIENT_EMAIL: Optional[str] = Field(env="FIREBASE_CLIENT_EMAIL")
    
    # API Keys (encrypted at rest, loaded at runtime)
    EXCHANGE_API_KEY: Optional[str] = Field(env="EXCHANGE_API_KEY")
    EXCHANGE_API_SECRET: Optional[str] = Field(env="EXCHANGE_API_SECRET")
    
    # Feature Engineering
    ENABLE_TECHNICAL_INDICATORS: bool = True
    ENABLE_ON_CHAIN_METRICS: bool = False  # Requires blockchain node
    ENABLE_SENTIMENT_ANALYSIS: bool = False  # Requires API
    
    @validator("FIREBASE_PROJECT_ID")
    def validate_firebase_config(cls, v, values):
        """Ensure Firebase config is present in production"""
        if values.get("ENVIRONMENT") == "production" and not v:
            raise ValueError("Firebase configuration required in production")
        return v
    
    @validator("EXCHANGE_API_KEY")
    def validate_exchange_config(cls, v, values):
        """Validate exchange credentials based on trading mode"""
        trading_mode = values.get("TRADING_MODE")
        if trading_mode == TradingMode.LIVE and not v:
            raise ValueError("Exchange API key required for live trading")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Feature flags for gradual rollout
FEATURE_FLAGS = {
    "enable_self_evolution": True,
    "enable_risk_management": True,
    "enable_cloud_sync": True,
    "enable_performance_monitoring": True,
}