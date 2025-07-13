// API Configuration
const API_BASE_URL = window.APP_CONFIG ? window.APP_CONFIG.API_BASE_URL : 'http://localhost:8000';

// Debug logging
console.log('API_BASE_URL:', API_BASE_URL);
console.log('Current hostname:', window.location.hostname);
console.log('APP_CONFIG:', window.APP_CONFIG);

// Global variables
let currentStock = null;
let technicalData = null;
let fundamentalData = null;
let predictionData = null;
let priceChart = null;
let indicatorsChart = null;
let performanceChart = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Allow Enter key to trigger analysis
    document.getElementById('stockSymbol').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            analyzeStock();
        }
    });
    
    // Auto-analyze TSLA on load
    setTimeout(() => {
        analyzeStock();
    }, 500);
});

// Main function to analyze stock
async function analyzeStock() {
    const symbol = document.getElementById('stockSymbol').value.trim().toUpperCase();
    
    if (!symbol) {
        alert('Please enter a stock symbol');
        return;
    }
    
    currentStock = symbol;
    showLoading();
    
    try {
        // Fetch technical analysis
        await fetchTechnicalAnalysis(symbol);
        
        // Fetch fundamental analysis
        await fetchFundamentalAnalysis(symbol);
        
        // Update the dashboard
        updateDashboard();
        
        hideLoading();
        showDashboard();
        
    } catch (error) {
        console.error('Error analyzing stock:', error);
        hideLoading();
        alert('Error analyzing stock. Please try again.');
    }
}

// Fetch technical analysis data
async function fetchTechnicalAnalysis(symbol) {
    try {
        console.log(`Fetching technical analysis for ${symbol} from ${API_BASE_URL}/stocks/${symbol}`);
        const response = await fetch(`${API_BASE_URL}/stocks/${symbol}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Technical analysis response:', data);
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        technicalData = data;
        return data;
    } catch (error) {
        console.error('Error fetching technical analysis:', error);
        if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
            throw new Error('Cannot connect to API server. Please check if the server is running.');
        }
        throw error;
    }
}

// Fetch fundamental analysis data
async function fetchFundamentalAnalysis(symbol) {
    try {
        const response = await fetch(`${API_BASE_URL}/company/${symbol}`);
        const data = await response.json();
        
        if (data.error) {
            console.warn('Fundamental analysis error:', data.error);
            fundamentalData = { error: data.error };
            return;
        }
        
        fundamentalData = data;
        return data;
    } catch (error) {
        console.error('Error fetching fundamental analysis:', error);
        fundamentalData = { error: error.message };
    }
}

// Fetch prediction data
async function getPrediction() {
    if (!currentStock) {
        alert('Please analyze a stock first');
        return;
    }
    
    const predictionButton = document.querySelector('#predictionResults button');
    predictionButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Getting Prediction...';
    predictionButton.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/predict/${currentStock}`);
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        predictionData = data;
        updatePredictionResults();
        
    } catch (error) {
        console.error('Error getting prediction:', error);
        document.getElementById('predictionResults').innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Error getting prediction: ${error.message}
            </div>
        `;
    } finally {
        predictionButton.innerHTML = '<i class="fas fa-magic me-2"></i>Get AI Prediction';
        predictionButton.disabled = false;
    }
}

// Update the main dashboard
function updateDashboard() {
    if (!technicalData) return;
    
    // Update stock info
    document.getElementById('stockName').textContent = `${currentStock} Analysis`;
    document.getElementById('stockSymbolDisplay').textContent = currentStock;
    
    // Update current price
    const currentPrice = technicalData.technical_summary.current_price;
    document.getElementById('currentPrice').textContent = `$${currentPrice.toFixed(2)}`;
    
    // Update key metrics
    document.getElementById('trendScore').textContent = `${technicalData.technical_summary.trend_score}/3`;
    document.getElementById('momentumScore').textContent = `${technicalData.technical_summary.momentum_score}/3`;
    document.getElementById('rsiValue').textContent = technicalData.technical_summary.rsi.toFixed(1);
    document.getElementById('macdValue').textContent = technicalData.technical_summary.macd.toFixed(2);
    
    // Update technical indicators table
    updateTechnicalIndicators();
    
    // Update fundamental analysis table
    updateFundamentalAnalysis();
    
    // Update trading signals
    updateTradingSignals();
    
    // Generate basic recommendation
    generateBasicRecommendation();
    
    // Create charts
    createCharts();
}

// Update technical indicators table
function updateTechnicalIndicators() {
    const indicators = technicalData.indicators;
    const tbody = document.getElementById('technicalIndicators');
    
    const technicalRows = [
        { label: 'Current Price', value: `$${indicators.close.toFixed(2)}`, type: 'neutral' },
        { label: 'SMA (20)', value: `$${indicators.SMA_20.toFixed(2)}`, type: getIndicatorType(indicators.close, indicators.SMA_20) },
        { label: 'SMA (50)', value: `$${indicators.SMA_50.toFixed(2)}`, type: getIndicatorType(indicators.close, indicators.SMA_50) },
        { label: 'EMA (12)', value: `$${indicators.EMA_12.toFixed(2)}`, type: getIndicatorType(indicators.close, indicators.EMA_12) },
        { label: 'RSI', value: indicators.RSI.toFixed(1), type: getRSIType(indicators.RSI) },
        { label: 'MACD', value: indicators.MACD.toFixed(2), type: getIndicatorType(indicators.MACD, 0) },
        { label: 'Bollinger Upper', value: `$${indicators.BB_Upper.toFixed(2)}`, type: 'neutral' },
        { label: 'Bollinger Lower', value: `$${indicators.BB_Lower.toFixed(2)}`, type: 'neutral' },
        { label: 'ATR', value: indicators.ATR.toFixed(2), type: 'neutral' },
        { label: 'Volume', value: formatVolume(indicators.volume), type: 'neutral' }
    ];
    
    tbody.innerHTML = technicalRows.map(row => `
        <tr>
            <td><strong>${row.label}</strong></td>
            <td class="indicator-${row.type}">${row.value}</td>
        </tr>
    `).join('');
}

// Update fundamental analysis table
function updateFundamentalAnalysis() {
    const tbody = document.getElementById('fundamentalAnalysis');
    
    if (!fundamentalData || fundamentalData.error) {
        tbody.innerHTML = `
            <tr>
                <td colspan="2" class="text-center text-muted">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Fundamental data not available
                </td>
            </tr>
        `;
        return;
    }
    
    const basicInfo = fundamentalData.basic_info || {};
    const valuation = fundamentalData.valuation_ratios || {};
    const profitability = fundamentalData.profitability_ratios || {};
    const financial = fundamentalData.financial_health || {};
    
    const fundamentalRows = [
        { label: 'Company Name', value: basicInfo.company_name || 'N/A' },
        { label: 'Sector', value: basicInfo.sector || 'N/A' },
        { label: 'Market Cap', value: formatMarketCap(basicInfo.market_cap) },
        { label: 'P/E Ratio', value: valuation.PE_ratio ? valuation.PE_ratio.toFixed(2) : 'N/A' },
        { label: 'P/B Ratio', value: valuation.PB_ratio ? valuation.PB_ratio.toFixed(2) : 'N/A' },
        { label: 'ROE', value: profitability.ROE ? (profitability.ROE * 100).toFixed(1) + '%' : 'N/A' },
        { label: 'ROA', value: profitability.ROA ? (profitability.ROA * 100).toFixed(1) + '%' : 'N/A' },
        { label: 'Altman Z-Score', value: financial.altman_z_score ? financial.altman_z_score.toFixed(2) : 'N/A' },
        { label: 'Piotroski Score', value: financial.piotroski_score ? `${financial.piotroski_score}/9` : 'N/A' },
        { label: 'Dividend Yield', value: basicInfo.dividend_yield ? (basicInfo.dividend_yield * 100).toFixed(2) + '%' : 'N/A' }
    ];
    
    tbody.innerHTML = fundamentalRows.map(row => `
        <tr>
            <td><strong>${row.label}</strong></td>
            <td>${row.value}</td>
        </tr>
    `).join('');
}

// Update prediction results
function updatePredictionResults() {
    if (!predictionData) return;
    
    const container = document.getElementById('predictionResults');
    
    // Calculate ensemble price target
    const currentPrice = predictionData.current_price;
    const ensembleData = predictionData.ensemble_prediction || {};
    const targetPrice = ensembleData.ensemble_prediction || currentPrice;
    const confidence = ensembleData.confidence || 0.5;
    
    let html = `
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="price-target">
                    <h4><i class="fas fa-target me-2"></i>Price Target</h4>
                    <div class="prediction-value">$${targetPrice.toFixed(2)}</div>
                    <div class="confidence-level">
                        Confidence: ${(confidence * 100).toFixed(1)}%
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card prediction-card">
                    <div class="card-body text-center">
                        <h5><i class="fas fa-robot me-2"></i>AI Recommendation</h5>
                        <div class="prediction-value">${predictionData.recommendation}</div>
                        <p class="mb-0">Current: $${currentPrice.toFixed(2)}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h6><i class="fas fa-chart-line me-2"></i>Price Movement</h6>
                        <div class="performance-metric">
                            <span>Expected Change:</span>
                            <span class="performance-value ${targetPrice > currentPrice ? '' : 'negative'}">
                                ${((targetPrice - currentPrice) / currentPrice * 100).toFixed(2)}%
                            </span>
                        </div>
                        <div class="performance-metric">
                            <span>Risk Level:</span>
                            <span class="performance-value ${confidence > 0.7 ? '' : 'negative'}">
                                ${confidence > 0.7 ? 'Low' : confidence > 0.5 ? 'Medium' : 'High'}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <h6><i class="fas fa-cogs me-2"></i>Model Performance Details</h6>
                <div class="row">
    `;
    
    // Display individual model results
    if (predictionData.training_results) {
        let modelCount = 0;
        for (const [model, results] of Object.entries(predictionData.training_results)) {
            if (!results.error && modelCount < 6) {
                const modelName = model.replace('_', ' ').toUpperCase();
                const r2Score = results.r2 || 0;
                const rmse = results.rmse || 0;
                
                html += `
                    <div class="col-md-6 mb-3">
                        <div class="model-performance">
                            <h6>${modelName}</h6>
                            <div class="performance-metric">
                                <span>R² Score:</span>
                                <span class="performance-value">${r2Score.toFixed(3)}</span>
                            </div>
                            <div class="performance-metric">
                                <span>RMSE:</span>
                                <span class="performance-value">${rmse.toFixed(2)}</span>
                            </div>
                        </div>
                    </div>
                `;
                modelCount++;
            }
        }
    }
    
    html += `
                </div>
            </div>
            <div class="col-md-6">
                <h6><i class="fas fa-info-circle me-2"></i>Technical Analysis Summary</h6>
                <div class="alert alert-info">
                    <h6>Key Insights:</h6>
                    <ul class="mb-0">
                        <li>Trend Score: ${technicalData.technical_summary.trend_score}/3</li>
                        <li>Momentum Score: ${technicalData.technical_summary.momentum_score}/3</li>
                        <li>RSI Level: ${technicalData.technical_summary.rsi.toFixed(1)} (${technicalData.technical_summary.rsi > 70 ? 'Overbought' : technicalData.technical_summary.rsi < 30 ? 'Oversold' : 'Neutral'})</li>
                        <li>MACD Signal: ${technicalData.technical_summary.macd > 0 ? 'Bullish' : 'Bearish'}</li>
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Create performance chart
    createModelPerformanceChart();
}

// Update trading signals
function updateTradingSignals() {
    const signals = technicalData.technical_summary.signals || [];
    const container = document.getElementById('tradingSignals');
    
    if (signals.length === 0) {
        container.innerHTML = `
            <div class="signal-item neutral">
                <i class="fas fa-info-circle me-2"></i>
                No significant trading signals detected
            </div>
        `;
        return;
    }
    
    const signalHtml = signals.map(signal => {
        const type = getSignalType(signal);
        return `
            <div class="signal-item ${type}">
                <i class="fas fa-${getSignalIcon(type)} me-2"></i>
                ${signal}
            </div>
        `;
    }).join('');
    
    container.innerHTML = signalHtml;
}

// Generate basic recommendation
function generateBasicRecommendation() {
    const summary = technicalData.technical_summary;
    let recommendation = 'HOLD';
    let reasoning = 'Mixed signals detected. ';
    
    // Simple recommendation logic
    if (summary.trend_score >= 2 && summary.momentum_score >= 2 && summary.rsi < 70) {
        recommendation = 'BUY';
        reasoning = 'Strong upward trend with good momentum. ';
    } else if (summary.trend_score <= 1 && summary.momentum_score <= 1 && summary.rsi > 30) {
        recommendation = 'SELL';
        reasoning = 'Weak trend with declining momentum. ';
    }
    
    // RSI considerations
    if (summary.rsi > 70) {
        reasoning += 'Stock may be overbought. ';
    } else if (summary.rsi < 30) {
        reasoning += 'Stock may be oversold. ';
    }
    
    // Update recommendation display
    const badge = document.getElementById('recommendationBadge');
    const text = document.getElementById('recommendationText');
    
    badge.textContent = recommendation;
    badge.className = `recommendation-badge ${recommendation}`;
    text.textContent = reasoning;
}

// Helper functions
function getIndicatorType(value1, value2) {
    if (value1 > value2) return 'positive';
    if (value1 < value2) return 'negative';
    return 'neutral';
}

function getRSIType(rsi) {
    if (rsi > 70) return 'negative'; // Overbought
    if (rsi < 30) return 'positive'; // Oversold
    return 'neutral';
}

function getSignalType(signal) {
    if (signal.includes('Oversold') || signal.includes('Below')) return 'bullish';
    if (signal.includes('Overbought') || signal.includes('Above')) return 'bearish';
    return 'neutral';
}

function getSignalIcon(type) {
    switch (type) {
        case 'bullish': return 'arrow-up';
        case 'bearish': return 'arrow-down';
        default: return 'minus';
    }
}

function formatVolume(volume) {
    if (volume >= 1000000) {
        return (volume / 1000000).toFixed(1) + 'M';
    } else if (volume >= 1000) {
        return (volume / 1000).toFixed(1) + 'K';
    }
    return volume.toString();
}

function formatMarketCap(marketCap) {
    if (!marketCap || marketCap === 0) return 'N/A';
    
    if (marketCap >= 1000000000000) {
        return `$${(marketCap / 1000000000000).toFixed(1)}T`;
    } else if (marketCap >= 1000000000) {
        return `$${(marketCap / 1000000000).toFixed(1)}B`;
    } else if (marketCap >= 1000000) {
        return `$${(marketCap / 1000000).toFixed(1)}M`;
    }
    return `$${marketCap.toFixed(0)}`;
}

// UI helper functions
function showLoading() {
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loadingIndicator').style.display = 'none';
}

function showDashboard() {
    document.getElementById('dashboard').style.display = 'block';
}

// Create charts for visualization
function createCharts() {
    if (!technicalData) return;
    
    createPriceChart();
    createIndicatorsChart();
}

// Create price chart with technical indicators
function createPriceChart() {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    // Destroy existing chart
    if (priceChart) {
        priceChart.destroy();
    }
    
    // Mock historical data for demonstration
    const labels = [];
    const prices = [];
    const sma20 = [];
    const sma50 = [];
    
    // Generate mock data points
    for (let i = 20; i >= 0; i--) {
        labels.push(`Day ${21-i}`);
        const basePrice = technicalData.technical_summary.current_price;
        prices.push(basePrice + (Math.random() - 0.5) * 20);
        sma20.push(technicalData.indicators.SMA_20 + (Math.random() - 0.5) * 10);
        sma50.push(technicalData.indicators.SMA_50 + (Math.random() - 0.5) * 15);
    }
    
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Price',
                    data: prices,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderWidth: 2,
                    fill: true
                },
                {
                    label: 'SMA 20',
                    data: sma20,
                    borderColor: '#28a745',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [5, 5]
                },
                {
                    label: 'SMA 50',
                    data: sma50,
                    borderColor: '#ffc107',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [10, 5]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: `${currentStock} - Price & Moving Averages`
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Price ($)'
                    }
                }
            }
        }
    });
}

// Create indicators chart (RSI and MACD)
function createIndicatorsChart() {
    const ctx = document.getElementById('indicatorsChart').getContext('2d');
    
    // Destroy existing chart
    if (indicatorsChart) {
        indicatorsChart.destroy();
    }
    
    // Mock historical data for RSI and MACD
    const labels = [];
    const rsiData = [];
    const macdData = [];
    
    for (let i = 20; i >= 0; i--) {
        labels.push(`Day ${21-i}`);
        rsiData.push(technicalData.technical_summary.rsi + (Math.random() - 0.5) * 20);
        macdData.push(technicalData.technical_summary.macd + (Math.random() - 0.5) * 2);
    }
    
    indicatorsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'RSI',
                    data: rsiData,
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    borderWidth: 2,
                    yAxisID: 'y'
                },
                {
                    label: 'MACD',
                    data: macdData,
                    borderColor: '#6f42c1',
                    backgroundColor: 'rgba(111, 66, 193, 0.1)',
                    borderWidth: 2,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: `${currentStock} - Technical Indicators`
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'RSI'
                    },
                    min: 0,
                    max: 100
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'MACD'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            }
        }
    });
}

// Create model performance chart
function createModelPerformanceChart() {
    if (!predictionData || !predictionData.training_results) return;
    
    const ctx = document.getElementById('modelPerformanceChart').getContext('2d');
    
    // Destroy existing chart
    if (performanceChart) {
        performanceChart.destroy();
    }
    
    const models = [];
    const r2Scores = [];
    const rmseValues = [];
    
    for (const [modelName, results] of Object.entries(predictionData.training_results)) {
        if (!results.error) {
            models.push(modelName.replace('_', ' ').toUpperCase());
            r2Scores.push(results.r2 || 0);
            rmseValues.push(results.rmse || 0);
        }
    }
    
    performanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: models,
            datasets: [
                {
                    label: 'R² Score',
                    data: r2Scores,
                    backgroundColor: 'rgba(40, 167, 69, 0.8)',
                    borderColor: '#28a745',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'RMSE',
                    data: rmseValues,
                    backgroundColor: 'rgba(220, 53, 69, 0.8)',
                    borderColor: '#dc3545',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Model Performance Metrics'
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'R² Score'
                    },
                    min: 0,
                    max: 1
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'RMSE'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            }
        }
    });
}
