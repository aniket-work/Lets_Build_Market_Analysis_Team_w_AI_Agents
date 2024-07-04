# Model names
LLAMA3_70B_8192 = "llama3-70b-8192"
CREWAI_LLAMA3_8B = "crewai-llama3-8b"

# API keys
GROQ_API_KEY = "GROQ_API_KEY"

# URLs
OLLAMA_BASE_URL = "http://localhost:11434/v1"

# Timeouts
REQUEST_TIMEOUT = 300000

# Placeholder API key
PLACEHOLDER_API_KEY = "NA"

# Agent roles
FINANCIAL_ANALYST_ROLE = "The Best Financial Analyst"
RESEARCH_ANALYST_ROLE = "Staff Research Analyst"
INVESTMENT_ADVISOR_ROLE = "Private Investment Advisor"

# Agent goals
FINANCIAL_ANALYST_GOAL = """Impress all customers with your financial data 
and market trends analysis"""
RESEARCH_ANALYST_GOAL = """Being the best at gather, interpret data and amaze
your customer with it"""
INVESTMENT_ADVISOR_GOAL = """Impress your customers with full analyses over stocks
and completer investment recommendations"""

# Agent backstories
FINANCIAL_ANALYST_BACKSTORY = """The most seasoned financial analyst with 
lots of expertise in stock market analysis and investment
strategies that is working for a super important customer."""
RESEARCH_ANALYST_BACKSTORY = """Known as the BEST research analyst, you're
skilled in sifting through news, company announcements, 
and market sentiments. Now you're working on a super 
important customer"""
INVESTMENT_ADVISOR_BACKSTORY = """You're the most experienced investment advisor
and you combine various analytical insights to formulate
strategic investment advice. You are now working for
a super important customer you need to impress."""




# Constants
TOOL_10Q = "Search 10-Q form"
TOOL_10K = "Search 10-K form"
SEC_API_KEY = 'SEC_API_API_KEY'
FORM_10Q = "10-Q"
FORM_10K = "10-K"
QUERY_TICKER = "ticker:"
QUERY_FORM_TYPE = "formType:"
QUERY_FROM = "0"
QUERY_SIZE = "1"
QUERY_SORT_FIELD = "filedAt"
QUERY_SORT_ORDER = "desc"
ERROR_NO_FILING = "Sorry, I couldn't find any filing for this stock, check if the ticker is correct."
SEPARATOR = "\n"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4

# Headers
HEADER_ACCEPT = 'Accept'
HEADER_ACCEPT_ENCODING = 'Accept-Encoding'
HEADER_ACCEPT_LANGUAGE = 'Accept-Language'
HEADER_CACHE_CONTROL = 'Cache-Control'
HEADER_DNT = 'Dnt'
HEADER_SEC_CH_UA = 'Sec-Ch-Ua'
HEADER_SEC_CH_UA_MOBILE = 'Sec-Ch-Ua-Mobile'
HEADER_SEC_CH_UA_PLATFORM = 'Sec-Ch-Ua-Platform'
HEADER_SEC_FETCH_DEST = 'Sec-Fetch-Dest'
HEADER_SEC_FETCH_MODE = 'Sec-Fetch-Mode'
HEADER_SEC_FETCH_SITE = 'Sec-Fetch-Site'
HEADER_SEC_FETCH_USER = 'Sec-Fetch-User'
HEADER_UPGRADE_INSECURE_REQUESTS = 'Upgrade-Insecure-Requests'
HEADER_USER_AGENT = 'User-Agent'

# Header values
ACCEPT_VALUE = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
ACCEPT_ENCODING_VALUE = 'gzip, deflate, br'
ACCEPT_LANGUAGE_VALUE = 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7'
CACHE_CONTROL_VALUE = 'max-age=0'
DNT_VALUE = '1'
SEC_CH_UA_VALUE = '"Not_A Brand";v="8", "Chromium";v="120"'
SEC_CH_UA_MOBILE_VALUE = '?0'
SEC_CH_UA_PLATFORM_VALUE = '"macOS"'
SEC_FETCH_DEST_VALUE = 'document'
SEC_FETCH_MODE_VALUE = 'navigate'
SEC_FETCH_SITE_VALUE = 'none'
SEC_FETCH_USER_VALUE = '?1'
UPGRADE_INSECURE_REQUESTS_VALUE = '1'
USER_AGENT_VALUE = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
