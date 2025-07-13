"""
Fundamental analysis module for calculating financial ratios and metrics.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import yfinance as yf
from datetime import datetime, timedelta

class FundamentalAnalysis:
    """Class for fundamental analysis calculations"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.stock = yf.Ticker(symbol)
        self._info = None
        self._financials = None
        self._balance_sheet = None
        self._cash_flow = None
    
    @property
    def info(self) -> Dict[str, Any]:
        """Get stock info from yfinance"""
        if self._info is None:
            try:
                self._info = self.stock.info
            except Exception:
                self._info = {}
        return self._info
    
    @property
    def financials(self) -> pd.DataFrame:
        """Get financial statements"""
        if self._financials is None:
            try:
                self._financials = self.stock.financials
            except Exception:
                self._financials = pd.DataFrame()
        return self._financials
    
    @property
    def balance_sheet(self) -> pd.DataFrame:
        """Get balance sheet"""
        if self._balance_sheet is None:
            try:
                self._balance_sheet = self.stock.balance_sheet
            except Exception:
                self._balance_sheet = pd.DataFrame()
        return self._balance_sheet
    
    @property
    def cash_flow(self) -> pd.DataFrame:
        """Get cash flow statement"""
        if self._cash_flow is None:
            try:
                self._cash_flow = self.stock.cashflow
            except Exception:
                self._cash_flow = pd.DataFrame()
        return self._cash_flow
    
    def get_valuation_ratios(self) -> Dict[str, float]:
        """Calculate valuation ratios"""
        info = self.info
        ratios = {}
        
        # Price ratios
        ratios['PE_ratio'] = info.get('trailingPE', 0)
        ratios['Forward_PE'] = info.get('forwardPE', 0)
        ratios['PB_ratio'] = info.get('priceToBook', 0)
        ratios['PS_ratio'] = info.get('priceToSalesTrailing12Months', 0)
        ratios['PEG_ratio'] = info.get('pegRatio', 0)
        
        # Market metrics
        ratios['Market_Cap'] = info.get('marketCap', 0)
        ratios['Enterprise_Value'] = info.get('enterpriseValue', 0)
        ratios['EV_Revenue'] = info.get('enterpriseToRevenue', 0)
        ratios['EV_EBITDA'] = info.get('enterpriseToEbitda', 0)
        
        return ratios
    
    def get_profitability_ratios(self) -> Dict[str, float]:
        """Calculate profitability ratios"""
        info = self.info
        ratios = {}
        
        # Margins
        ratios['Gross_Margin'] = info.get('grossMargins', 0)
        ratios['Operating_Margin'] = info.get('operatingMargins', 0)
        ratios['Net_Margin'] = info.get('profitMargins', 0)
        
        # Returns
        ratios['ROE'] = info.get('returnOnEquity', 0)
        ratios['ROA'] = info.get('returnOnAssets', 0)
        ratios['ROIC'] = info.get('returnOnCapital', 0)
        
        return ratios
    
    def get_liquidity_ratios(self) -> Dict[str, float]:
        """Calculate liquidity ratios"""
        balance_sheet = self.balance_sheet
        ratios = {}
        
        if not balance_sheet.empty and len(balance_sheet.columns) > 0:
            latest_bs = balance_sheet.iloc[:, 0]
            
            current_assets = latest_bs.get('Total Current Assets', 0)
            current_liabilities = latest_bs.get('Total Current Liabilities', 0)
            cash = latest_bs.get('Cash And Cash Equivalents', 0)
            inventory = latest_bs.get('Inventory', 0)
            
            # Current ratio
            if current_liabilities != 0:
                ratios['Current_Ratio'] = current_assets / current_liabilities
            else:
                ratios['Current_Ratio'] = 0
            
            # Quick ratio
            if current_liabilities != 0:
                ratios['Quick_Ratio'] = (current_assets - inventory) / current_liabilities
            else:
                ratios['Quick_Ratio'] = 0
            
            # Cash ratio
            if current_liabilities != 0:
                ratios['Cash_Ratio'] = cash / current_liabilities
            else:
                ratios['Cash_Ratio'] = 0
        else:
            ratios = {'Current_Ratio': 0, 'Quick_Ratio': 0, 'Cash_Ratio': 0}
        
        return ratios
    
    def get_leverage_ratios(self) -> Dict[str, float]:
        """Calculate leverage ratios"""
        balance_sheet = self.balance_sheet
        ratios = {}
        
        if not balance_sheet.empty and len(balance_sheet.columns) > 0:
            latest_bs = balance_sheet.iloc[:, 0]
            
            total_debt = latest_bs.get('Total Debt', 0)
            total_equity = latest_bs.get('Total Stockholder Equity', 0)
            total_assets = latest_bs.get('Total Assets', 0)
            
            # Debt-to-equity ratio
            if total_equity != 0:
                ratios['Debt_to_Equity'] = total_debt / total_equity
            else:
                ratios['Debt_to_Equity'] = 0
            
            # Debt-to-assets ratio
            if total_assets != 0:
                ratios['Debt_to_Assets'] = total_debt / total_assets
            else:
                ratios['Debt_to_Assets'] = 0
            
            # Equity multiplier
            if total_equity != 0:
                ratios['Equity_Multiplier'] = total_assets / total_equity
            else:
                ratios['Equity_Multiplier'] = 0
        else:
            ratios = {'Debt_to_Equity': 0, 'Debt_to_Assets': 0, 'Equity_Multiplier': 0}
        
        return ratios
    
    def get_growth_metrics(self) -> Dict[str, float]:
        """Calculate growth metrics"""
        info = self.info
        metrics = {}
        
        # Growth rates
        metrics['Revenue_Growth'] = info.get('revenueGrowth', 0)
        metrics['Earnings_Growth'] = info.get('earningsGrowth', 0)
        metrics['EPS_Growth'] = info.get('earningsQuarterlyGrowth', 0)
        
        return metrics
    
    def calculate_altman_z_score(self) -> float:
        """Calculate Altman Z-Score for bankruptcy prediction"""
        balance_sheet = self.balance_sheet
        financials = self.financials
        
        if balance_sheet.empty or financials.empty:
            return 0.0
        
        try:
            latest_bs = balance_sheet.iloc[:, 0]
            latest_fin = financials.iloc[:, 0]
            
            # Get required values
            working_capital = latest_bs.get('Total Current Assets', 0) - latest_bs.get('Total Current Liabilities', 0)
            total_assets = latest_bs.get('Total Assets', 1)  # Avoid division by zero
            retained_earnings = latest_bs.get('Retained Earnings', 0)
            ebit = latest_fin.get('Operating Income', 0)
            market_cap = self.info.get('marketCap', 0)
            total_liabilities = latest_bs.get('Total Liab', 0)
            sales = latest_fin.get('Total Revenue', 0)
            
            # Calculate Z-Score components
            a = working_capital / total_assets
            b = retained_earnings / total_assets
            c = ebit / total_assets
            d = market_cap / total_liabilities if total_liabilities != 0 else 0
            e = sales / total_assets
            
            # Altman Z-Score formula
            z_score = 1.2 * a + 1.4 * b + 3.3 * c + 0.6 * d + 1.0 * e
            
            return z_score
        except Exception:
            return 0.0
    
    def calculate_piotroski_score(self) -> int:
        """Calculate Piotroski F-Score (0-9)"""
        info = self.info
        balance_sheet = self.balance_sheet
        financials = self.financials
        cash_flow = self.cash_flow
        
        score = 0
        
        try:
            # Profitability (4 points)
            if info.get('returnOnAssets', 0) > 0:
                score += 1
            if not cash_flow.empty and cash_flow.iloc[0, 0] > 0:  # Operating cash flow > 0
                score += 1
            if info.get('returnOnAssets', 0) > 0:  # ROA improvement (simplified)
                score += 1
            if not cash_flow.empty and cash_flow.iloc[0, 0] > financials.iloc[0, 0]:  # Cash flow > net income
                score += 1
            
            # Leverage/Liquidity (3 points)
            if not balance_sheet.empty and len(balance_sheet.columns) > 1:
                current_debt = balance_sheet.iloc[:, 0].get('Total Debt', 0)
                previous_debt = balance_sheet.iloc[:, 1].get('Total Debt', 0)
                if current_debt < previous_debt:  # Debt decreased
                    score += 1
            
            current_ratio = self.get_liquidity_ratios().get('Current_Ratio', 0)
            if current_ratio > 1.5:  # Good liquidity
                score += 1
            
            # Efficiency (2 points)
            if info.get('grossMargins', 0) > 0.3:  # Good gross margin
                score += 1
            if info.get('operatingMargins', 0) > 0.1:  # Good operating margin
                score += 1
            
        except Exception:
            pass
        
        return min(score, 9)  # Cap at 9
    
    def get_comprehensive_analysis(self) -> Dict[str, Any]:
        """Get comprehensive fundamental analysis"""
        return {
            'basic_info': {
                'symbol': self.symbol,
                'company_name': self.info.get('longName', ''),
                'sector': self.info.get('sector', ''),
                'industry': self.info.get('industry', ''),
                'market_cap': self.info.get('marketCap', 0),
                'current_price': self.info.get('currentPrice', 0),
                'dividend_yield': self.info.get('dividendYield', 0)
            },
            'valuation_ratios': self.get_valuation_ratios(),
            'profitability_ratios': self.get_profitability_ratios(),
            'liquidity_ratios': self.get_liquidity_ratios(),
            'leverage_ratios': self.get_leverage_ratios(),
            'growth_metrics': self.get_growth_metrics(),
            'financial_health': {
                'altman_z_score': self.calculate_altman_z_score(),
                'piotroski_score': self.calculate_piotroski_score()
            }
        }

def get_fundamental_summary(symbol: str) -> Dict[str, Any]:
    """
    Get a comprehensive fundamental analysis summary for a stock
    
    Args:
        symbol: Stock symbol
        
    Returns:
        Dictionary with fundamental analysis summary
    """
    try:
        analyzer = FundamentalAnalysis(symbol)
        return analyzer.get_comprehensive_analysis()
    except Exception as e:
        print(f"Error in fundamental analysis for {symbol}: {e}")
        return {
            'error': str(e),
            'symbol': symbol
        }
