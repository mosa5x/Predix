from django.http import JsonResponse
from django.core.cache import cache
import logging
from .tasks import ARABIC_STOCK_NAMES, ARABIC_COMMODITY_NAMES, COMMODITIES, CRYPTOCURRENCIES, ARABIC_CRYPTOCURRENCIES_NAMES

logger = logging.getLogger(__name__)

from .tasks import ARABIC_STOCK_NAMES

logger = logging.getLogger(__name__)

def get_stock_data(request, stock):
    result = cache.get(f'latest_scrape_result_{stock}', {})
    logger.info(f"Retrieved data for {stock} from cache: {result}")
    return JsonResponse(result)

def get_all_stocks(request):
    stocks = [
                'apple', 'amazon', 'microsoft', 'facebook', 'microsoft', 'netflix', 'nokia', 'nvidia', 'paypal', 'pinterest', 'tesla', 'amd', 'alibaba', 'boeing', 'disney', 'ibm'
        ]
    results = []
    for stock in stocks:
        result = cache.get(f'latest_scrape_result_{stock}', {})
        logger.info(f"Retrieved data for {stock} from cache: {result}")
        results.append({
            'stock': stock,
            'data': result
        })
    logger.info(f"Returning all stock data: {results}")
    return JsonResponse({'stocks': results})
def get_stocks(request):
    stocks = [
        'apple', 'amazon', 'microsoft', 'facebook', 'netflix', 'nokia', 'nvidia', 
        'paypal', 'pinterest', 'tesla', 'amd', 'alibaba', 'boeing', 'disney', 'ibm'
    ]
    arabic_names = [ARABIC_STOCK_NAMES.get(stock, stock) for stock in stocks]
    return JsonResponse({
        'stocks': stocks,
        'arabic_names': arabic_names
    })

def get_commodities(request):
    commodities = COMMODITIES
    arabic_names = [ARABIC_COMMODITY_NAMES.get(commodity, commodity) for commodity in commodities]
    return JsonResponse({
        'commodities': commodities,
        'arabic_names': arabic_names
    })

def get_commodity_data(request, commodity):
    result = cache.get(f'latest_scrape_result_{commodity}', {})
    logger.info(f"Retrieved data for {commodity} from cache: {result}")
    return JsonResponse(result)

def get_all_commodities(request):
    results = []
    for commodity in COMMODITIES:
        result = cache.get(f'latest_scrape_result_{commodity}', {})
        logger.info(f"Retrieved data for {commodity} from cache: {result}")
        results.append({
            'commodity': commodity,
            'data': result
        })
    logger.info(f"Returning all commodity data: {results}")
    return JsonResponse({'commodities': results})

def get_cryptocurrencies(request):
    cryptocurrencies = CRYPTOCURRENCIES
    arabic_names = [ARABIC_CRYPTOCURRENCIES_NAMES.get(crypto, crypto) for crypto in cryptocurrencies]
    return JsonResponse({
        'cryptocurrencies': cryptocurrencies,
        'arabic_names': arabic_names
    })

def get_cryptocurrency_data(request, crypto):
    result = cache.get(f'latest_scrape_result_{crypto}', {})
    logger.info(f"Retrieved data for {crypto} from cache: {result}")
    return JsonResponse(result)

def get_all_cryptocurrencies(request):
    results = []
    for crypto in CRYPTOCURRENCIES:
        result = cache.get(f'latest_scrape_result_{crypto}', {})
        logger.info(f"Retrieved data for {crypto} from cache: {result}")
        results.append({
            'cryptocurrency': crypto,
            'data': result
        })
    logger.info(f"Returning all cryptocurrency data: {results}")
    return JsonResponse({'cryptocurrencies': results})