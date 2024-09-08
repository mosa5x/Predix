from celery import shared_task
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from celery.utils.log import get_task_logger
from django.core.cache import cache
from datetime import datetime
import pytz
import re
from typing import List, Dict
import logging
from typing import Dict

logger = get_task_logger(__name__)

ARABIC_STOCK_NAMES = {
    'apple': 'آبل',
    'amazon': 'أمازون',
    'microsoft': 'مايكروسوفت',
    'facebook': 'فيسبوك',
    'netflix': 'نتفليكس',
    'nokia': 'نوكيا',
    'nvidia': 'إنفيديا',
    'paypal': 'باي بال',
    'pinterest': 'بينتيريست',
    'tesla': 'تسلا',
    'amd': 'إيه إم دي',
    'alibaba': 'علي بابا',
    'boeing': 'بوينغ',
    'disney': 'ديزني',
    'ibm': 'آي بي إم',
    'aramco': 'أرامكو',
    'v-stock': 'فيزا',
    'uber-stock': 'أوبر',
    'spot-stock': 'سبوتيفاي',
    'lcid-stock': 'لوسيد',
    'intc-stock': 'إنتل',
    'dell-stock': 'ديل',
    'adbe-stock': 'أدوبي',
    'abnb-stock': 'إير بي إن بي'

}


ARABIC_NAMES = [
    'آبل',
    'أمازون',
    'مايكروسوفت',
    'فيسبوك',
    'مايكروسوفت',
    'نتفليكس',
    'نوكيا',
    'إنفيديا',
    'باي بال',
    'بينتيريست',
    'تسلا',
    'إيه إم دي',
    'علي بابا',
    'بوينغ',
    'ديزني',
    'آي بي إم',
    'أرامكو',
    'فيزا',
    'أوبر',
    'سبوتيفاي',
    'لوسيد',
    'إنتل',
    'ديل',
    'أدوبي',
    'إير بي إن بي'
]


COMMODITIES = ['gold', 'oil', 'silver']
ARABIC_COMMODITY_NAMES = {
    'gold': 'الذهب',
    'oil': 'النفط',
    'silver': 'الفضة'
}

CRYPTOCURRENCIES = ['btc']  # Add more as needed
ARABIC_CRYPTOCURRENCIES_NAMES = {
    'btc': 'بيتكوين',

    # Add more as needed
}

ARABIC_DAYS = {
    'Monday': 'الاثنين',
    'Tuesday': 'الثلاثاء',
    'Wednesday': 'الأربعاء',
    'Thursday': 'الخميس',
    'Friday': 'الجمعة',
    'Saturday': 'السبت',
    'Sunday': 'الأحد'
}

ARABIC_MONTHS = {
    "January": "يناير", "February": "فبراير", "March": "مارس",
    "April": "أبريل", "May": "مايو", "June": "يونيو",
    "July": "يوليو", "August": "أغسطس", "September": "سبتمبر",
    "October": "أكتوبر", "November": "نوفمبر", "December": "ديسمبر"
}




def translate_forecast(text, stock_name):
    sentences = text.split('. ')
    translated_sentences = []
    
    for sentence in sentences:
        
        
        closed_previous_match = re.match(r'(\w+) stock closed the previous day at \$(\d+(?:\.\d+)?), which is \$(\d+(?:\.\d+)?) (higher|lower) than 30 days ago and \$(\d+(?:\.\d+)?) (higher|lower) than 7 days ago', text)
        if closed_previous_match:
            _, close_price, thirty_day_diff, thirty_day_direction, seven_day_diff, seven_day_direction = closed_previous_match.groups()
            thirty_day_arabic = "أعلى" if thirty_day_direction == "higher" else "أقل"
            seven_day_arabic = "أعلى" if seven_day_direction == "higher" else "أقل"
            return (
                f"أغلق سهم {ARABIC_STOCK_NAMES.get(stock_name.lower(), stock_name)} في اليوم السابق عند {close_price} دولار. "
                f"هذا السعر {thirty_day_arabic} بـ {thirty_day_diff} دولار مما كان عليه قبل 30 يومًا، "
                f"و{seven_day_arabic} بـ {seven_day_diff} دولار مما كان عليه قبل 7 أيام."
            )
        
        # Handle "In X weeks" sentences
        if sentence.startswith("In "):
            parts = sentence.split(" ", 3)
            if len(parts) >= 4:
                weeks = parts[1]
                rest = parts[3]
                arabic_weeks = {
                    "1": "الأسبوع الأول",
                    "2": "الأسبوع الثاني",
                    "3": "الأسبوع الثالث",
                    "4": "الأسبوع الرابع"
                }.get(weeks, f"{weeks} أسابيع")
                translated_sentence = f"في {arabic_weeks} {translate_forecast(rest, stock_name)}"
                translated_sentences.append(translated_sentence)
                continue

        # Handle monthly forecasts
        monthly_match = re.match(r'(\w+) (?:stock price forecast|stock prediction) for (\w+) (\d{4}) in the weeks at ([\d.]+) Maximum ([\d.]+), minimum ([\d.]+) The averaged price ([\d.]+) At the end of the month ([\d.]+) dollars, change for (\w+) ([-\d.]+)%', sentence)
        if monthly_match:
            stock, month, year, start, max_price, min_price, avg_price, end_price, change_month, change_percent = monthly_match.groups()
            arabic_sentence = f"توقعات سعر سهم {ARABIC_STOCK_NAMES.get(stock_name.lower(), stock_name)} لشهر {ARABIC_MONTHS.get(month, month)} {year}: السعر في بداية الشهر {start} دولار، الحد الأعلى {max_price}، الحد الأدنى {min_price}. متوسط السعر {avg_price} دولار. في نهاية الشهر {end_price} دولار، بتغيير {change_percent}% خلال {ARABIC_MONTHS.get(change_month, change_month)}."
            translated_sentences.append(arabic_sentence)
            continue

        # Handle daily forecasts
        daily_match = re.match(r'(\w+) stock (?:price forecast|prediction) (?:on|for) (\w+), (\w+), (\d+): ([\d.]+) dollars, maximum ([\d.]+), minimum ([\d.]+)', sentence)
        if daily_match:
            _, day, month, date, price, max_price, min_price = daily_match.groups()
            day_ar = ARABIC_DAYS.get(day, day)
            month_ar = ARABIC_MONTHS.get(month, month)
            
            arabic_sentence = f"توقعات سعر سهم {ARABIC_STOCK_NAMES.get(stock_name.lower(), stock_name)} يوم {day_ar} {date} {month_ar}: {price} دولار (الحد الأعلى: {max_price}، الحد الأدنى: {min_price}), "
            translated_sentences.append(arabic_sentence)
            continue

        # If no specific format matches, translate key terms
        for day_en, day_ar in ARABIC_DAYS.items():
            sentence = sentence.replace(day_en, day_ar)
        for month_en, month_ar in ARABIC_MONTHS.items():
            sentence = sentence.replace(month_en, month_ar)
        
        sentence = sentence.replace(stock_name.capitalize(), ARABIC_STOCK_NAMES.get(stock_name.lower(), stock_name))
        sentence = sentence.replace("stock price forecast", "توقعات سعر السهم")
        sentence = sentence.replace("stock prediction", "توقعات السهم")
        sentence = sentence.replace("dollars", "دولار")
        sentence = sentence.replace("maximum", "الحد الأعلى")
        sentence = sentence.replace("minimum", "الحد الأدنى")
        sentence = sentence.replace(" on ", " يوم ")
        sentence = sentence.replace("At the end of the month", "في نهاية الشهر")
        sentence = sentence.replace("change for", "التغيير لشهر")
        
        translated_sentences.append(sentence)
    
    return ' '.join(translated_sentences)

def translate_table(table_data):
    translated_table = []
    
    header = ['السعر المتوقع', 'الحد الأعلى', 'الحد الأدنى', 'اليوم', 'التاريخ']
    translated_table.append(header)
    
    for row in table_data[1:]:  # Skip the original header
        translated_row = [
            row[4],   # Price
            row[3],   # Max
            row[2],   # Min
            ARABIC_DAYS.get(row[1], row[1]),  # Translated day name
            row[0],   # Date
        ]
        translated_table.append(translated_row)
    
    return translated_table

@shared_task
def scrape_and_translate(stock):
    logger.info(f"Starting scrape and translate for {stock}")
    log_current_time.delay()  # Log the time when the task starts

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=chrome_options
    )
    
    elements = {
        "date": "/html/body/div/div/div/div/main/article/div/strong",
        "closed_the_previous": "/html/body/div/div/div/div/main/article/div/p[1]",
        "table": "/html/body/div/div/div/div/main/article/div/div[1]/div[1]/table",
        "p1": "/html/body/div/div/div/div/main/article/div/p[2]",
        "p2": "/html/body/div/div/div/div/main/article/div/p[3]",
        "p4": "/html/body/div/div/div/div/main/article/div/p[6]",
        "p5": "/html/body/div/div/div/div/main/article/div/p[7]",
        "p6": "/html/body/div/div/div/div/main/article/div/p[8]",
    }

    try:
        driver.get(f"https://30rates.com/{stock}")
        logger.info(f"Navigated to https://30rates.com/{stock}")
        
        wait = WebDriverWait(driver, 10)
        result = {}

        arabic_stock_name = ARABIC_STOCK_NAMES.get(stock.lower(), stock)

        for key, xpath in elements.items():
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                if key == "table":
                    try:
                        rows = element.find_elements(By.TAG_NAME, "tr")
                        table_data = []
                        
                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, "td") or row.find_elements(By.TAG_NAME, "th")
                            table_data.append([cell.text for cell in cells])
                        
                        translated_table_data = translate_table(table_data)
                        
                        result[key] = {
                            'original': table_data,
                            'translated': translated_table_data
                        }
                        logger.info(f"Scraped table {key} for {stock}: {table_data[:2]}...")
                    except Exception as e:
                        logger.error(f"Error scraping table {key} for {stock}: {str(e)}")
                        logger.error(f"HTML content of table {key}: {element.get_attribute('outerHTML')}")
                        result[key] = {'original': 'Error scraping data', 'translated': 'خطأ في استخراج البيانات'}
                else:
                    text = element.text
                    translated_text = translate_forecast(text, stock)
                    result[key] = {
                        'original': text,
                        'translated': translated_text
                    }
                logger.info(f"Scraped and translated {key} for {stock}: {result[key]}")
            except Exception as e:
                logger.error(f"Error scraping {key} for {stock}: {str(e)}")
                result[key] = {'original': 'Error scraping data', 'translated': 'خطأ في استخراج البيانات'}

        logger.info(f"Completed scraping and translating for {stock}")
        cache.set(f'latest_scrape_result_{stock}', result, timeout=None)
        logger.info(f"Stored result in cache for {stock}")

        return result

    except Exception as e:
        logger.error(f"An error occurred while scraping {stock}: {str(e)}")
        return None

    finally:
        driver.quit()
        logger.info(f"Closed WebDriver for {stock}")

@shared_task
def log_current_time():
    utc_time = datetime.now(pytz.utc)
    iraq_time = utc_time.astimezone(pytz.timezone('Asia/Baghdad'))
    logger.info(f"Current UTC time: {utc_time}")
    logger.info(f"Current Iraq time: {iraq_time}")


def get_commodity_url(commodity: str) -> str:
    if commodity == 'silver':
        return f"https://30rates.com/{commodity}-price-forecast"
    return f"https://30rates.com/{commodity}-price-forecast-and-predictions"


def translate_commodity_table(table_data):
    translated_table = []
    
    header = ['السعر المتوقع', 'الحد الأعلى', 'الحد الأدنى', 'اليوم', 'التاريخ']
    translated_table.append(header)
    
    for row in table_data[1:]:  # Skip the original header
        translated_row = [
            row[4],   # Price
            row[3],   # Max
            row[2],   # Min
            ARABIC_DAYS.get(row[1], row[1]),  # Translated day name
            row[0],   # Date
        ]
        translated_table.append(translated_row)
    
    return translated_table

def translate_date(date_string):
    parts = date_string.split('/')
    if len(parts) == 2:
        day, month = parts
        return f"{day}/{ARABIC_MONTHS.get(month, month)}"
    return date_string

COMMODITY_XPATHS = {
    'oil': {
        'table': "/html/body/div/div/div/div/main/article/div/div[1]/div[1]/table/tbody"
    },
    'gold': {
        'table': "/html/body/div/div/div/div/main/article/div/div[3]/div[1]/table/tbody"
    },
    'silver': {
        'table': "/html/body/div/div/div/div/main/article/div/div[3]/div[1]/table/tbody"
    }
}

CRYPTOCURRENCIES_XPATHS = {
    'btc': {
        'table': "/html/body/div/div/div/div/main/article/div/div[3]/div[1]/table"
    },
    # Add more cryptocurrencies and their specific XPaths if needed
}




import re
import logging

logger = logging.getLogger(__name__)



def translate_commodity_forecast(text, commodity_name):
    try:
        # Handle oil
        if commodity_name == "oil":
            match = re.search(r'Brent crude oil price equal to ([\d.]+) Dollars per 1 barrell\.\. Today\'s price range: ([\d.]+ - [\d.]+)\.\. The previous day close: ([\d.]+), the change was ([-+]?[\d.]+), ([-+]?[\d.]+%)', text)
            if match:
                price, price_range, close_price, change, percentage = match.groups()
                translated_text = (
                    f"سعر نفط برنت الخام يساوي {price} دولار للبرميل. "
                    f"نطاق السعر اليوم: {price_range}. "
                    f"إغلاق اليوم السابق: {close_price} دولار، التغير كان {change} دولار ({percentage})"
                )
                return translated_text

        # Handle gold and silver
        elif commodity_name in ["gold", "silver"]:
            match = re.search(r'Actual (\w+) price equal to ([\d.]+) Dollars per troy ounce or ([\d.]+) Dollars per 1 gram\.\. Today\'s price range: ([\d.]+ - [\d.]+)\.\. The previous day close: \$?([\d.]+), the change was ([-+][\d.]+), ([-+][\d.]+%)', text)
            if match:
                _, price_per_ounce, price_per_gram, price_range, close_price, change, percentage = match.groups()
                translated_text = (
                    f"السعر الفعلي لـ {ARABIC_COMMODITY_NAMES.get(commodity_name, commodity_name)} يساوي {price_per_ounce} دولار للأونصة أو {price_per_gram} دولار للجرام. "
                    f"نطاق السعر اليوم: {price_range}. "
                    f"إغلاق اليوم السابق: {close_price} دولار، التغير كان {change} دولار ({percentage})"
                )
                return translated_text

        # If it doesn't match the intro format, proceed with the original translation logic
        sentences = text.split('. ')
        translated_sentences = []
        
        for sentence in sentences:
            # Handle daily forecasts
            daily_match = re.match(r'(\w+) price (?:forecast|prediction) on (\w+), (\w+), (\d+): ([\d.]+) Dollars, maximum ([\d.]+), minimum ([\d.]+)', sentence)
            if daily_match:
                commodity, day, month, date, price, max_price, min_price = daily_match.groups()
                day_ar = ARABIC_DAYS.get(day, day)
                month_ar = ARABIC_MONTHS.get(month, month)
                
                arabic_sentence = f"توقعات سعر {ARABIC_COMMODITY_NAMES.get(commodity_name, commodity_name)} يوم {day_ar} {date} {month_ar}: {price} دولار (الحد الأعلى: {max_price}، الحد الأدنى: {min_price})"
                translated_sentences.append(arabic_sentence)
                continue

            # Handle "In X weeks" sentences
            weeks_match = re.match(r'In (\d+) weeks? (.+)', sentence)
            if weeks_match:
                weeks, rest = weeks_match.groups()
                arabic_weeks = {
                    "1": "الأسبوع الأول",
                    "2": "الأسبوع الثاني",
                    "3": "الأسبوع الثالث",
                    "4": "الأسبوع الرابع"
                }.get(weeks, f"{weeks} أسابيع")
                translated_sentence = f"في {arabic_weeks} {translate_commodity_forecast(rest, commodity_name)}"
                translated_sentences.append(translated_sentence)
                continue

            # If no specific format matches, just clean the sentence
            cleaned_sentence = re.sub(r'\b[a-zA-Z]+\b', '', sentence)
            cleaned_sentence = cleaned_sentence.replace('$', '').replace('l', '').replace('to', '').replace('ounce', '')
            if cleaned_sentence.strip():
                translated_sentences.append(cleaned_sentence.strip())
        
        result = ' '.join(filter(bool, translated_sentences))
        if not result:
            raise ValueError("No valid translation produced")
        return result
    except Exception as e:
        logger.error(f"Error translating {commodity_name} forecast: {str(e)}")
        return f"خطأ في ترجمة توقعات {ARABIC_COMMODITY_NAMES.get(commodity_name, commodity_name)}"


@shared_task
def scrape_and_translate_commodity(commodity: str) -> Dict:
    logger.info(f"Starting scrape and translate for {commodity}")
    log_current_time.delay()  # Log the time when the task starts

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=chrome_options
    )
    


    try:


        elements = {
        "date": "/html/body/div/div/div/div/main/article/div/h2[1]",
        "intro": "/html/body/div/div/div/div/main/article/div/p[1]",
        "table": (COMMODITY_XPATHS.get(commodity, {}).get('table', "//table")),
        "p1": "//main//article//div/p[2]",
        "p2": "//main//article//div/p[3]",
        "p3": "//main//article//div/p[6]",
        "p4": "//main//article//div/p[7]",
        "p5": "//main//article//div/p[8]",
        }
        url = get_commodity_url(commodity)
        driver.get(url)
        logger.info(f"Navigated to {url}")
        
        wait = WebDriverWait(driver, 10)
        result = {}

        arabic_commodity_name = ARABIC_COMMODITY_NAMES.get(commodity.lower(), commodity)

        for key, xpath in elements.items():
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                if key == "table":
                    rows = element.find_elements(By.TAG_NAME, "tr")
                    table_data = []
                    
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td") or row.find_elements(By.TAG_NAME, "th")
                        table_data.append([cell.text for cell in cells])
                    
                    translated_table_data = translate_commodity_table(table_data)
                    
                    result[key] = {
                        'original': table_data,
                        'translated': translated_table_data
                    }
                    print(table_data)
                    print(translated_table_data)

                elif key.startswith("p") or key == "intro":
                    text = element.text
                    # Split the text into sentences and rejoin with a period and space
                    sentences = re.split(r'(?<=[.!?])\s+', text)
                    text = '. '.join(sentence.strip() for sentence in sentences if sentence.strip())
                    translated_text = translate_commodity_forecast(text, commodity)
                    result[key] = {
                        'original': text,
                        'translated': translated_text
                    }
                else:
                    text = element.text
                    if key == "date":
                        # Remove the commodity price today part
                        text = re.sub(r'\s*\w+\s+Price\s+Today\.?', '', text, flags=re.IGNORECASE)
                        translated_text = f"تاريخ التحديث: {text.strip()}"
                    else:
                        translated_text = text
                    result[key] = {
                        'original': text,
                        'translated': translated_text
                    }
                logger.info(f"Scraped and translated {key} for {commodity}: {result[key]}")
            except Exception as e:
                logger.error(f"Error scraping {key} for {commodity}: {str(e)}")
                result[key] = {'original': 'Error scraping data', 'translated': 'خطأ في استخراج البيانات'}

        logger.info(f"Completed scraping and translating for {commodity}")
        cache.set(f'latest_scrape_result_{commodity}', result, timeout=None)
        logger.info(f"Stored result in cache for {commodity}")

        return result

    except Exception as e:
        logger.error(f"An error occurred while scraping {commodity}: {str(e)}")
        return None

    finally:
        driver.quit()
        logger.info(f"Closed WebDriver for {commodity}")



def get_cryptocurrency_url(crypto: str) -> str:
    return f"https://30rates.com/{crypto}-to-usd-forecast-today-dollar-to-bitcoin"




logger = logging.getLogger(__name__)

def translate_cryptocurrency_forecast(text: str, crypto_name: str) -> str:
    try:
        # Remove the unwanted parts
        text = re.sub(r'^\d{4}/\d{2}/\d{2}\.\s*', '', text)  # Remove date at the beginning
        text = text.replace(f"{crypto_name} Price Today", "").strip()  # Remove "Bitcoin Price Today"
        
        sentences = text.split('. ')
        translated_sentences = []
        
        for sentence in sentences:
            # Skip the "Inverse rate" sentence
            if sentence.startswith("Inverse rate:"):
                continue

            # Handle daily forecasts
            daily_match = re.match(r'(\w+) (?:price prediction|forecast) on (\w+), (\w+), (\d+): price ([\d.]+) dollars, maximum ([\d.]+), minimum ([\d.]+)', sentence)
            if daily_match:
                crypto, day, month, date, price, max_price, min_price = daily_match.groups()
                day_ar = ARABIC_DAYS.get(day, day)
                month_ar = ARABIC_MONTHS.get(month, month)
                
                arabic_sentence = f"توقعات سعر {ARABIC_CRYPTOCURRENCIES_NAMES.get(crypto_name, crypto_name)} يوم {day_ar} {date} {month_ar}: {price} دولار (الحد الأعلى: {max_price} دولار، الحد الأدنى: {min_price} دولار)"
                translated_sentences.append(arabic_sentence)
                continue

            # Handle "In X weeks" sentences
            weeks_match = re.match(r'In (\d+) weeks? (.+)', sentence)
            if weeks_match:
                weeks, rest = weeks_match.groups()
                arabic_weeks = {
                    "1": "الأسبوع الأول",
                    "2": "الأسبوع الثاني",
                    "3": "الأسبوع الثالث",
                    "4": "الأسبوع الرابع"
                }.get(weeks, f"{weeks} أسابيع")
                translated_sentence = f"في {arabic_weeks}: {translate_cryptocurrency_forecast(rest, crypto_name)}"
                translated_sentences.append(translated_sentence)
                continue

            # Handle "price equal to" sentences
            if "price equal to" in sentence:
                match = re.search(r'(\w+) price equal to (\d+\.?\d*) dollars a coin', sentence)
                if match:
                    crypto, price = match.groups()
                    translated_sentence = f"السعر الحالي لـ {ARABIC_CRYPTOCURRENCIES_NAMES.get(crypto_name, crypto_name)} هو {price} دولار للعملة الواحدة"
                    translated_sentences.append(translated_sentence)
                continue

            # Handle "Today's traded price range" sentences
            price_range_match = re.search(r"Today's traded price range: ([\d.]+ - [\d.]+)", sentence)
            if price_range_match:
                price_range = price_range_match.group(1)
                translated_sentence = f"نطاق سعر التداول اليوم: {price_range} دولار"
                translated_sentences.append(translated_sentence)
                continue

            # Handle "The previous day close" sentences
            if "The previous day close:" in sentence:
                match = re.search(r'The previous day close: ([\d.]+)', sentence)
                if match:
                    close_price = match.group(1)
                    translated_sentence = f"سعر الإغلاق في اليوم السابق: {close_price} دولار"
                    translated_sentences.append(translated_sentence)
                continue

            # Handle "The change was" sentences
            if "The change was" in sentence:
                match = re.search(r'The change was ([-\d.]+), ([-\d.]+%)', sentence)
                if match:
                    change, percentage = match.groups()
                    translated_sentence = f"كان التغير {change} دولار ({percentage})"
                    translated_sentences.append(translated_sentence)
                continue

            # If no specific format matches, keep the original sentence
            translated_sentences.append(sentence)
        
        result = ' '.join(filter(bool, translated_sentences))
        if not result:
            raise ValueError("No valid translation produced")
        return result
    except Exception as e:
        logger.error(f"Error translating {crypto_name} forecast: {str(e)}")
        return f"حدث خطأ أثناء ترجمة توقعات {ARABIC_CRYPTOCURRENCIES_NAMES.get(crypto_name, crypto_name)}"

def translate_date(date_string: str) -> str:
    parts = date_string.split('/')
    if len(parts) == 2:
        day, month = parts
        return f"{day}/{ARABIC_MONTHS.get(month, month)}"
    return date_string

@shared_task
def scrape_and_translate_cryptocurrency(crypto: str) -> Dict:
    logger.info(f"Starting scrape for {crypto}")
    log_current_time.delay()  # Log the time when the task starts

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=chrome_options
    )

    try:
        elements = {
            "date": "/html/body/div/div/div/div/main/article/div/h2[1]",
            "intro": "/html/body/div/div/div/div/main/article/div/p[1]",
            "table": (CRYPTOCURRENCIES_XPATHS.get(crypto, {}).get('table', "//table")),
            "p1": "/html/body/div/div/div/div/main/article/div/p[2]",
            "p2": "/html/body/div/div/div/div/main/article/div/p[3]",
            "p3": "/html/body/div/div/div/div/main/article/div/p[6]",
            "p4": "/html/body/div/div/div/div/main/article/div/p[7]",
            "p5": "/html/body/div/div/div/div/main/article/div/p[8]",
        }
        url = get_cryptocurrency_url(crypto)
        driver.get(url)
        logger.info(f"Navigated to {url}")
        
        wait = WebDriverWait(driver, 10)
        result = {}

        for key, xpath in elements.items():
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                if key == "table":
                    rows = element.find_elements(By.TAG_NAME, "tr")
                    table_data = []
                    
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td") or row.find_elements(By.TAG_NAME, "th")
                        table_data.append([cell.text for cell in cells])
                    
                    result[key] = {
                        'original': table_data,
                        'translated': translate_commodity_table(table_data)  # You might need to create a similar function for cryptocurrencies
                    }
                elif key == "date":
                    text = element.text
                    # Remove "Bitcoin Price Today" or similar phrases
                    cleaned_text = re.sub(r'\s*\w+\s+Price\s+Today', '', text, flags=re.IGNORECASE)
                    date_match = re.search(r'\d{4}/\d{2}/\d{2}', cleaned_text)
                    if date_match:
                        translated_text = f"تاريخ التحديث: {date_match.group()}"
                    else:
                        translated_text = f"تاريخ التحديث: {cleaned_text}"
                    result[key] = {
                        'original': text,
                        'translated': translated_text
                    }
                elif key.startswith("p") or key == "intro":
                    text = element.text
                    translated_text = translate_cryptocurrency_forecast(text, crypto)
                    result[key] = {
                        'original': text,
                        'translated': translated_text
                    }
                else:
                    text = element.text
                    translated_text = text
                    result[key] = {
                        'original': text,
                        'translated': translated_text
                    }
                logger.info(f"Scraped and translated {key} for {crypto}: {result[key]}")
            except Exception as e:
                logger.error(f"Error scraping {key} for {crypto}: {str(e)}")
                result[key] = {'original': 'Error scraping data', 'translated': 'خطأ في استخراج البيانات'}

        logger.info(f"Completed scraping for {crypto}")
        cache.set(f'latest_scrape_result_{crypto}', result, timeout=None)
        logger.info(f"Stored result in cache for {crypto}")
        print(result)

        return result

    except Exception as e:
        logger.error(f"An error occurred while scraping {crypto}: {str(e)}")
        return None

    finally:
        driver.quit()
        logger.info(f"Closed WebDriver for {crypto}")

@shared_task
def scrape_all_cryptocurrencies():
    logger.info("Starting scrape_all_cryptocurrencies task")
    log_current_time.delay()
    for crypto in CRYPTOCURRENCIES:
        scrape_and_translate_cryptocurrency.delay(crypto)
        logger.info(f"Queued scraping task for {crypto}")
    logger.info("Finished queueing all cryptocurrency scraping tasks")

@shared_task
def scrape_all_commodities():
    logger.info("Starting scrape_all_commodities task")
    log_current_time.delay()
    for commodity in COMMODITIES:
        scrape_and_translate_commodity.delay(commodity)
        logger.info(f"Queued scraping task for {commodity}")
    logger.info("Finished queueing all commodity scraping tasks")


@shared_task
def scrape_all_stocks():
    logger.info("Starting scrape_all_stocks task")
    log_current_time.delay()  # Log the time when the task starts
    stocks = ['apple', 'amazon'  ]
    for stock in stocks:
        scrape_and_translate.delay(stock)
        logger.info(f"Queued scraping task for {stock}")
    logger.info("Finished queueing all stock scraping tasks")

@shared_task
def check_cache_contents():
    logger.info("Starting check_cache_contents task")
    stocks = ['apple', 'amazon', 'microsoft', 'facebook', 'microsoft', 'netflix', 'nokia', 'nvidia',
               'paypal', 'pinterest', 'tesla', 'amd', 'alibaba', 'boeing', 'disney', 'ibm' , 'aramco',
               'v-stock','uber-stock','spot-stock', 'lcid-stock','intc-stock','dell-stock','adbe-stock',
               'abnb-stock'
                 ]
    for stock in stocks:
        result = cache.get(f'latest_scrape_result_{stock}')
        if result:
            logger.info(f"Cache content for {stock}: {result}")
        else:
            logger.info(f"No cache content found for {stock}")
    logger.info("Finished checking cache contents")












