import logging
import re
import time
from typing import Dict, List, Optional, Union
import requests

from ..parser.exceptions import RobotException
from ..utils.url_utils import get_supported_protocol, normalize_url, validate_url

class RobotParser:
    """
    A class for parsing robots.txt files and checking rules for web crawlers.
    Follows Google guidelines for robots.txt parsing.
    """

    def __init__(self):
        self._url: str = ""
        self.robot_content: Optional[str] = None
        self._cache: Dict[str, str] = {}
        self._cache_ttl: int = 3600  # 1 hour cache TTL

    def set_url(self, url: str) -> None:
        """
        Set the URL for the parser.
        
        Args:
            url (str): The URL to set
        """
        if url is not None:
            self._url = normalize_url(url)
            self.robot_content = None

    @property
    def url(self) -> str:
        """Get the current URL."""
        return self._url

    def get_robot(self, url: str) -> Optional[str]:
        """
        Fetch the robots.txt file for a given URL.
        
        Args:
            url (str): The URL to fetch robots.txt from
            
        Returns:
            Optional[str]: The content of robots.txt or None if fetch fails
        """
        try:
            url = normalize_url(url)
            if url in self._cache:
                return self._cache[url]

            time.sleep(3)  # Rate limiting
            logging.info(f"Fetching robots.txt from: {url}/robots.txt")
            
            response = requests.get(
                f"{url}/robots.txt",
                verify=True,
                timeout=10
            )
            response.encoding = "utf-8"
            
            if not (200 <= response.status_code < 300):
                return f"Error: HTTP Status Code {response.status_code}"
                
            content = response.text
            self._cache[url] = content
            return content

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching robots.txt: {e}")
            return None

    def parse(self, url: str, action: str) -> Optional[Union[Dict, List[str]]]:
        """
        Parse robots.txt content for specific actions.
        
        Args:
            url (str): The URL to parse
            action (str): The action to perform ('crawl_delay', 'sitemaps', 'user_agent')
            
        Returns:
            Optional[Union[Dict, List[str]]]: Parsed results based on action
        """
        if self.robot_content is None:
            self.robot_content = self.get_robot(url)
            if self.robot_content is None:
                return None

        if action == "crawl_delay":
            return self._parse_crawl_delay()
        elif action == "sitemaps":
            return self._parse_sitemaps()
        elif action == "user_agent":
            return self._parse_user_agent()
        else:
            return None

    def _parse_crawl_delay(self) -> Dict[str, Dict[str, Optional[str]]]:
        """Parse crawl delay directives."""
        if not self.robot_content:
            return {}
            
        user_agent_blocks = re.split(r"(?=\bUser-agent:)", self.robot_content)
        user_agent_blocks = [block.strip() for block in user_agent_blocks if block.strip()]
        
        result = {}
        for block in user_agent_blocks:
            lines = block.split("\n")
            user_agent = lines[0].replace("User-agent:", "").strip()
            crawl_delay = None
            
            for line in lines[1:]:
                line = line.strip().lower()
                if line.startswith("crawl-delay:"):
                    crawl_delay = line.replace("crawl-delay:", "").strip()
                    
            result[user_agent] = {
                "user_agent": user_agent,
                "crawl_delay": crawl_delay,
            }
            
        return result

    def _parse_sitemaps(self) -> List[str]:
        """Parse sitemap directives."""
        if not self.robot_content:
            return []
            
        return re.findall(r'(?im)^sitemap:\s*(https?://\S+)', self.robot_content)

    def _parse_user_agent(self) -> List[Dict[str, Dict[str, List[str]]]]:
        """Parse user-agent directives."""
        if not self.robot_content:
            return []
            
        lines = [line for line in self.robot_content.split("\n") 
                if not line.startswith("#")]
        result_text = "\n".join(lines)
        user_agent_blocks = re.split(r"(?=\buser-agent:)", result_text.lower())
        user_agent_blocks = [block.strip() for block in user_agent_blocks if block.strip()]
        
        blocks_list = []
        for block in user_agent_blocks:
            lines = block.split("\n")
            user_agent = lines[0].replace("user-agent:", "").strip()
            allowed = []
            disallowed = []
            
            for line in lines[1:]:
                line = line.strip()
                if line.startswith("allow:"):
                    allowed.append(line.replace("allow:", "").strip())
                elif line.startswith("disallow:"):
                    disallowed.append(line.replace("disallow:", "").strip())
                    
            blocks_list.append({user_agent: {"allowed": allowed, "disallowed": disallowed}})
            
        return blocks_list

    def check_for_rule(self, user_agent: str, path: str) -> bool:
        """
        Check if a path is allowed for a specific user-agent.
        
        Args:
            user_agent (str): The user-agent to check
            path (str): The path to check
            
        Returns:
            bool: True if path is allowed, False otherwise
        """
        if not self.robot_content:
            return True
            
        specific_block = self.get_specific_block(
            self.parse(self._url, "user_agent"),
            user_agent
        )
        
        if not specific_block:
            return True
            
        return self.match_rules(specific_block, path)

    @staticmethod
    def get_specific_block(blocks: Optional[List[Dict]], user_agent: str) -> Optional[Dict]:
        """Get rules for a specific user-agent."""
        if not blocks:
            return None
            
        for block in blocks:
            if user_agent in block:
                return block[user_agent]
        return None

    def get_sitemaps(self) -> List[str]:
        """Get all sitemap URLs."""
        return self.parse(self._url, "sitemaps") or []

    def match_rules(self, specific_block: Dict, path: str) -> bool:
        """Match path against allow/disallow rules."""
        allowed = specific_block.get("allowed", [])
        disallowed = specific_block.get("disallowed", [])
        
        if not allowed and not disallowed:
            return True
            
        reg_str = re.escape(path)
        return (self.match_allow_rules(allowed, path, reg_str) or
                not self.match_disallow_rules(disallowed, path, reg_str))

    @staticmethod
    def match_allow_rules(rules: List[str], path: str, reg_str: str) -> bool:
        """Match path against allow rules."""
        for rule in rules:
            if rule == "/":
                return True
            if rule.endswith("$") and path == rule[:-1]:
                return True
            if rule.endswith("*"):
                if path.startswith(rule[:-1]):
                    return True
            if path.startswith(rule):
                return True
        return False

    @staticmethod
    def match_disallow_rules(rules: List[str], path: str, reg_str: str) -> bool:
        """Match path against disallow rules."""
        for rule in rules:
            if rule == "/":
                return True
            if rule.endswith("$") and path == rule[:-1]:
                return True
            if rule.endswith("*"):
                if path.startswith(rule[:-1]):
                    return True
            if path.startswith(rule):
                return True
        return False

    def get_crawl_delay(self, user_agent: str) -> Optional[float]:
        """
        Get crawl delay for a specific user-agent.
        
        Args:
            user_agent (str): The user-agent to get crawl delay for
            
        Returns:
            Optional[float]: Crawl delay in seconds or None if not specified
        """
        delays = self.parse(self._url, "crawl_delay")
        if not delays:
            return None
            
        for agent, data in delays.items():
            if agent == user_agent:
                delay = data.get("crawl_delay")
                return float(delay) if delay else None
                
        return None 