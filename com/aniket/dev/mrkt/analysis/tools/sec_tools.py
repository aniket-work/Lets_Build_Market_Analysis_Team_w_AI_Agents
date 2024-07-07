import os
import requests
from langchain.tools import tool
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from sec_api import QueryApi
from unstructured.partition.html import partition_html
from com.aniket.dev.mrkt.analysis.constant.constants import *

class SECTools():

    @tool(TOOL_10Q)
    def search_10q(data):
        """
    Useful to search information from the latest 10-Q form for a
    given stock.
    The input to this tool should be a pipe (|) separated text of
    length two, representing the stock ticker you are interested and what
    question you have from it.
       For example, `AAPL|what was last quarter's revenue`.
    """
        stock, ask = data.split("|")
        return SECTools.__search_form(stock, ask, FORM_10Q)

    @tool(TOOL_10K)
    def search_10k(data):
        """
    Useful to search information from the latest 10-K form for a
    given stock.
    The input to this tool should be a pipe (|) separated text of
    length two, representing the stock ticker you are interested, what
    question you have from it.
    For example, `AAPL|what was last year's revenue`.
    """
        stock, ask = data.split("|")
        return SECTools.__search_form(stock, ask, FORM_10K)

    @staticmethod
    def __search_form(stock, ask, form_type):
        queryApi = QueryApi(api_key=os.environ[SEC_API_KEY])
        query = {
            "query": {
                "query_string": {
                    "query": f"{QUERY_TICKER}{stock} AND {QUERY_FORM_TYPE}\"{form_type}\""
                }
            },
            "from": QUERY_FROM,
            "size": QUERY_SIZE,
            "sort": [{QUERY_SORT_FIELD: {"order": QUERY_SORT_ORDER}}]
        }

        filings = queryApi.get_filings(query)['filings']
        if len(filings) == 0:
            return ERROR_NO_FILING
        link = filings[0]['linkToFilingDetails']
        answer = SECTools.__embedding_search(link, ask)
        return answer

    @staticmethod
    def __embedding_search(url, ask):
        text = SECTools.__download_form_html(url)
        elements = partition_html(text=text)
        content = SEPARATOR.join([str(el) for el in elements])
        text_splitter = CharacterTextSplitter(
            separator=SEPARATOR,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            is_separator_regex=False,
        )
        docs = text_splitter.create_documents([content])
        retriever = FAISS.from_documents(
            docs, OpenAIEmbeddings()
        ).as_retriever()
        answers = retriever.get_relevant_documents(ask, top_k=TOP_K)
        answers = SEPARATOR.join([a.page_content for a in answers])
        return answers

    @staticmethod
    def __download_form_html(url):
        headers = {
            HEADER_ACCEPT: ACCEPT_VALUE,
            HEADER_ACCEPT_ENCODING: ACCEPT_ENCODING_VALUE,
            HEADER_ACCEPT_LANGUAGE: ACCEPT_LANGUAGE_VALUE,
            HEADER_CACHE_CONTROL: CACHE_CONTROL_VALUE,
            HEADER_DNT: DNT_VALUE,
            HEADER_SEC_CH_UA: SEC_CH_UA_VALUE,
            HEADER_SEC_CH_UA_MOBILE: SEC_CH_UA_MOBILE_VALUE,
            HEADER_SEC_CH_UA_PLATFORM: SEC_CH_UA_PLATFORM_VALUE,
            HEADER_SEC_FETCH_DEST: SEC_FETCH_DEST_VALUE,
            HEADER_SEC_FETCH_MODE: SEC_FETCH_MODE_VALUE,
            HEADER_SEC_FETCH_SITE: SEC_FETCH_SITE_VALUE,
            HEADER_SEC_FETCH_USER: SEC_FETCH_USER_VALUE,
            HEADER_UPGRADE_INSECURE_REQUESTS: UPGRADE_INSECURE_REQUESTS_VALUE,
            HEADER_USER_AGENT: USER_AGENT_VALUE
        }

        response = requests.get(url, headers=headers)
        return response.text