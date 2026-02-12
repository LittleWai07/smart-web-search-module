"""
SmartWebSearch.QueryStorm
~~~~~~~~~~~~

This module implements the query brainstorm for the web searching module.
"""

# Import the required modules
import json, os, sys, shutil, re
from typing import Any, TypeAlias, Literal
import requests

# QueryStorm Class
class QueryStorm:
    """
    A class for query brainstorming.
    """

    @staticmethod
    def __send_request(openai_comp_api_key: str, messages: list[dict[str, Any]], model: str = "deepseek-chat", openai_comp_api_base_url: str = "https://api.deepseek.com/chat/completions") -> dict[str, Any]:
        """
        Send a request to the OpenAI Compatible API.

        Args:
            openai_comp_api_key (str): The OpenAI Compatible API key.
            messages (list[dict[str, Any]]): The messages to send.
            model (str): The model to use.
            openai_comp_api_base_url (str): The OpenAI Compatible API base URL.

        Returns:
            dict[str, Any]: The response from the OpenAI Compatible API.
        """

        # Send a request to the OpenAI Compatible API
        res: requests.Response = requests.post(
            openai_comp_api_base_url,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_comp_api_key}"
            },
            json = {
                "model": model,
                "messages": messages
            }
        )

        # Raise an exception if the request fails
        res.raise_for_status()

        # Return the response
        return res.json()

    def __init__(self, openai_comp_api_key: str, model: str = "deepseek-chat", openai_comp_api_base_url: str = "https://api.deepseek.com/chat/completions") -> None:
        """
        Initialize the QueryStorm object.

        Args:
            openai_comp_api_key (str): The OpenAI Compatible API key.
            openai_comp_api_base_url (str): The OpenAI Compatible API base URL.

        Returns:
            None
        """

        # Set the attributes of the QueryStorm object
        self.model: str = model
        self.openai_comp_api_key: str = openai_comp_api_key
        self.openai_comp_api_base_url: str = openai_comp_api_base_url

    def storm_with_summary(self, query: str, summary: str) -> list[str]:
        """
        Generate a query based on the summary of the search results.

        Args:
            query (str): The search query.
            summary (str): The summary of the search results.

        Returns:
            list[str]: The generated queries.
        """

        prompt: str = """你是一个智能搜索助手，专门负责分析用户的搜索意图并生成扩展的搜索细节关键词。

        任务描述：
        根据用户提供的搜索关键词“{query}”和该关键词的搜索结果总结“{summary}”，首先判断用户想搜索的内容的核心类型（例如，概念定义、工具使用、历史背景、技术原理等），然后基于这个类型，延展出更多相关的搜索细节关键词。这些关键词应帮助用户进一步精确搜索，获取更具体、更深入的信息。

        输出格式要求：
        - 輸出3至5個搜索細節關鍵詞即可，不必太多，也不能太少。
        - 仅输出搜索细节关键词，不包含任何其他文字或解释。
        - 每个搜索细节关键词之间用一个空格“ ”隔开。
        - 如果搜索细节关键词内包含多个单词，请用加号“+”连接，不要使用空格或其他分隔符。
        - 所有搜索细节关键词必须使用英文。

        示例：
        输入：
        query = 三角函数
        summary = 三角函数是数学很常见的一类关于角度的函数。三角函数将直角三角形的内角和它的两边的比值相关联，亦可以用单位圆的各种有关线段的长短的等价来定义。三角函数在研究三角形和圆形等几何形状的性质时有着重要的作用，亦是研究振动、波、天体运动和各种周期性现象的基础数学工具。在数学分析上，三角函数亦定义为无穷级数或特定微分方程式的解，允许它们的取值扩展到任意实数值，甚至是复数值。
        输出：
        definitions purposes general+formulas

        请严格按照上述格式和示例执行。"""

        # Generate a query based on the summary of the search results
        res: dict[str, Any] = self.__send_request(
            self.openai_comp_api_key,
            [
                {
                    "role": "user",
                    "content": prompt.format(query = query, summary = summary)
                }
            ],
            self.model,
            self.openai_comp_api_base_url
        )

        # Return the generated queries
        return res["choices"][0]["message"]["content"].split(" ")