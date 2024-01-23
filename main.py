import logging
import re
import time
from urllib import parse

import requests


class RobotException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class RobotParser:
    """
    A simple class for parsing robots.txt files and checking rules for web crawlers.
    I followed google guidelines for robots.txt and not RFC 9309, but it's pretty similar
    """

    def __init__(self):
        self._url = ""
        self.robot_content = None

    @staticmethod
    def __validator__(url):
        if not isinstance(url, str):
            raise RobotException("Please provide a url")
        return url

    def set_url(self, url):
        if url is not None:
            self._url = url
            self.robot_content = None

    @property
    def get_url(self):
        return self._url

    @staticmethod
    def get_supported_protocol(url):
        if not re.match(r"^https?://", url):
            url = "http://" + url  # Add 'http://' if missing

        https_url = url.replace("http://", "https://")

        try:
            # Check if the server supports HTTPS
            response = requests.head(https_url)
            if response.status_code < 400:
                return "https"

            # If HTTPS is not supported, check if the server supports HTTP
            response = requests.head(url)
            if response.status_code < 400:
                return "http"

            return "Unsupported"  # Neither HTTP nor HTTPS supported

        except requests.exceptions.RequestException:
            return "http"

    @staticmethod
    def get_robot(url):
        """
        Fetches the robots.txt file for a given URL and returns its content.

        **Inputs**

        * url (str): The URL for which to fetch the robots.txt file.

        **Returns**

        * str: The content of the robots.txt file if successfully retrieved.
                 If an error occurs during the request, it returns None.

        This function sends a GET request to the provided URL and retrieves the content
        of the robots.txt file. It ensures that the URL is properly formatted with 'http://'
        if missing and checks for a successful HTTP status code (2xx) before returning
        the content. If an error occurs during the request, it logs the exception and
        returns None.

        Note:
            - Make sure to handle the returned content appropriately in your code.
            - You may want to handle exceptions more gracefully depending on your application's
              requirements.
        """
        try:
            # Check if the URL is valid
            # ret = RobotParser.get_supported_protocol(url)
            # url = f"{ret}://{url}"
            time.sleep(3)
            logging.info(f"Trying to get robot from url: {url}/robots.txt")
            response = requests.get(url + "/robots.txt", verify=True, timeout=10)
            response.encoding = "utf-8"
            if 200 > response.status_code >= 300:
                return f"Error: HTTP Status Code {response.status_code}"
            return response.text

        except requests.exceptions.RequestException as e:
            logging.info(f"Error request : {e}")
            return None

    def parse(self, url: str, action: str):
        """
        Parse the content of a robots.txt file for a given URL and extract information based on the specified action.

        **Inputs**

        * url (str): The URL for which to fetch and parse the robots.txt file. * action (str): The action to perform,
        which can be one of the following: 'crawl_delay', 'sitemaps', or 'user_agent'. Default is None. * user_agent
        (str, optional): The user-agent string to consider for the 'user_agent' action. Default is None.

        **Returns**

        * dict: A dictionary containing information extracted from the robots.txt file based on the specified action.

        This method fetches the robots.txt file for the provided URL and extracts relevant information based on the
        specified action. The supported actions are as follows:

        - 'crawl_delay': Extracts user-agents and their corresponding crawl delay values.
        - 'sitemaps': Extracts a list of sitemap URLs.
        - 'user_agent': Extracts user-agents and their corresponding allowed and disallowed paths.

        The extracted data is returned as a dictionary with user-agents as keys and corresponding information based
        on the action.
        """
        if self.robot_content is None:
            self.robot_content = self.get_robot(url)
            if self.robot_content is None:
                return None

        robots_txt = self.robot_content
        if action == "crawl_delay":
            user_agent_blocks = re.split(r"(?=\bUser-agent:)", robots_txt)

            # Remove leading and trailing whitespace from each block
            user_agent_blocks = [block.strip() for block in user_agent_blocks]

            # Filter out empty blocks
            user_agent_blocks = [block for block in user_agent_blocks if block]

            dict_blocks = {}

            # Process each block and extract allowed and disallowed paths
            for block in user_agent_blocks:
                # Split the block into lines
                lines = block.split("\n")
                # Remove leading and trailing whitespace from each line
                user_agent = lines[0].replace("User-agent:", "").strip()
                # Initialize the allowed and disallowed paths
                crawl_delay = None

                # Process each line
                for line in lines[1:]:
                    # Remove leading and trailing whitespace from each line
                    line = line.strip().lower()
                    if line.startswith("crawl-delay:"):
                        # Add the path to the allowed paths
                        crawl_delay = line.replace("crawl-delay:", "").strip()
                # Add the user-agent, allowed, and disallowed paths to the dictionary
                dict_blocks[user_agent] = {
                    "user_agent": user_agent,
                    "crawl_delay": crawl_delay,
                }
            return dict_blocks

        elif action == "sitemaps":
            sitemap = []
            sites = re.findall(
                r"(?i)(?<=sitemap: )https?:/{2}w[0-9a-zA-Z()@:%_+.~#?&/=]*\.[a-z]{1,4}$",
                robots_txt,
                re.MULTILINE,
            )

            sitemap.extend(sites)
            return sitemap

        elif action == "user_agent":
            lines = robots_txt.split("\n")

            # Filter out lines starting with '#'
            filtered_lines = [line for line in lines if not line.startswith("#")]

            # Join the filtered lines back into a single string
            result_text = "\n".join(filtered_lines)
            user_agent_blocks = re.split(r"(?=\buser-agent:)", result_text.lower())

            # Remove leading and trailing whitespace from each block
            user_agent_blocks = [block.strip() for block in user_agent_blocks]

            # Filter out empty blocks
            user_agent_blocks = [block for block in user_agent_blocks if block]

            blocks_list = []

            # Process each block and extract allowed and disallowed paths

            for block in user_agent_blocks:
                dict_blocks = {}
                # Split the block into lines
                lines = block.split("\n")
                # Remove leading and trailing whitespace from each line
                user_agent = lines[0].replace("User-agent:".lower(), "").strip()
                # Initialize the allowed and disallowed paths
                allowed = []
                disallowed = []

                # Process each line
                for line in lines[1:]:
                    # Remove leading and trailing whitespace from each line
                    line = line.strip()
                    if line.startswith("Allow:".lower()):
                        # Add the path to the allowed paths
                        allowed.append(line.replace("Allow:".lower(), "").strip())
                    elif line.startswith("Disallow:".lower()):
                        # Add the path to the disallowed paths
                        disallowed.append(line.replace("Disallow:".lower(), "").strip())

                # Add the user-agent, allowed, and disallowed paths to the dictionary
                dict_blocks[user_agent] = {"allowed": allowed, "disallowed": disallowed}
                blocks_list.append(dict_blocks)

            merged_dict = {}

            for item in blocks_list:
                for key, value in item.items():
                    if key in merged_dict:
                        # If the key already exists in the merged_dict, update the values.
                        merged_dict[key]["allowed"] += value["allowed"]
                        merged_dict[key]["disallowed"] += value["disallowed"]
                    else:
                        # If the key doesn't exist in the merged_dict, add it.
                        merged_dict[key] = value

            # Convert merged_dict back to a list of dictionaries
            merged_list = [{key: value} for key, value in merged_dict.items()]
            return merged_list
        else:
            return None

    @staticmethod
    def count_slashes(rule: str):
        """
        Count the number of slashes in a given rule.

        **Inputs**

        * rule (str): The rule for which to count slashes.

        **Returns**

        * int: The number of slashes in the provided rule.
        """
        # Count the number of slashes in the rule
        return rule.count("/")

    def check_for_rule(self, user_agent: str, path: str):
        """
        Check if a specific user-agent and path combination is allowed based on the robots.txt rules.

        **Inputs**

        * user_agent (str): The user-agent for which to check the rules.
        * path (str): The path to be checked for permission.

        **Returns**

        This function doesn't return a value. It processes the robots.txt rules and prints the result.
        """
        if self._url is not None:
            blocks = self.parse(self._url, action="user_agent")
            if blocks is None:
                # Http error, print an error message and exit
                return False, {"msg": "Error retrieving robots.txt"}

            blocks_dict = {}
            for block in blocks:
                blocks_dict.update(block)
            # Check if the user agent is in the robots.txt
            specific_block = self.get_specific_block(blocks_dict, user_agent.lower())
            print(f"specific_block: {specific_block}")
            if specific_block is None:
                return False, {"msg": "User agent not found in robots.txt"}

            # Check if the path is allowed for the user agent
            dict_rules_match = self.match_rules(specific_block, path)
            # Print the result
            return self.print_result(dict_rules_match, path, user_agent)

    @staticmethod
    def get_specific_block(blocks: dict | None, user_agent: str) -> dict | None:
        """
        Retrieve the rules specific to a user-agent from a dictionary of user-agent blocks.

        **Inputs**

        * blocks (dict): A dictionary containing user-agent blocks extracted from the robots.txt file.
        * user_agent (str): The user-agent for which to retrieve rules.

        **Returns**

        * dict or None: A dictionary of rules specific to the user-agent if found, or None if not found.
        """
        # Check if the specific user agent is in the robots.txt
        specific_block = blocks.get(user_agent, None)

        if specific_block is None:
            specific_block = blocks.get("*", None)
        return specific_block

    def get_sitemaps(self):
        """
        Retrieve and print the sitemap URLs for a given URL.

        **Inputs**

        This method doesn't take any input parameters other than the 'self' parameter.

        **Returns**

        * list or None: A list of sitemap URLs if successfully retrieved, or None if there was an HTTP error.
        """
        if self._url is not None:
            sitemaps = self.parse(self._url, action="sitemaps")
            if sitemaps is None:
                # Http error, print an error message and exit
                return None, {"sitemaps": None, "msg": "Error retrieving sitemaps"}
            else:
                return True, {"sitemaps": sitemaps}

    def match_rules(self, specific_block: dict, path: str):
        """
        Match the given path against the allowed and disallowed rules of a specific user-agent.

        **Inputs**

        * specific_block (dict): A dictionary containing allowed and disallowed rules for a specific user-agent.
        * path (str): The path to be matched against the rules.

        **Returns**

        * list: A list of matched rules based on the path.
        """
        # Regex for replacing the * wildcard
        reg_str = "[a-zA-Z0-9*._$?!&]*"
        # Extract the allowed and disallowed paths or None
        allow = specific_block.get("allowed") or None
        disallow = specific_block.get("disallowed") or None
        dict_rules_match = []

        if allow is not None:
            dict_rules_match.extend(self.match_allow_rules(allow, path, reg_str))

        if disallow is not None:
            dict_rules_match.extend(self.match_disallow_rules(disallow, path, reg_str))
        return dict_rules_match

    @staticmethod
    def match_allow_rules(rules: list, path: str, reg_str: str):
        """
        Match the provided path against a list of allowed rules.

        **Inputs**

        * rules (list): A list of allowed rules to be matched against.
        * path (str): The path to be matched against the rules.
        * reg_str (str): A regular expression string used for wildcard matching.

        **Returns**

        * list: A list of matched rules based on the path.
        """
        matched_rules = []
        for rule in rules:
            rule = parse.unquote(rule)
            if "*" in rule:
                rule_regex = rule.replace("*", reg_str)
                rule_regex = "^" + rule_regex
                match = re.match(rule_regex, path)
                if match is not None:
                    matched_rules.append(
                        {"status": "allowed", "rule": rule, "len": len(rule)}
                    )
            else:
                if rule == path:
                    matched_rules.append(
                        {"status": "allowed", "rule": rule, "len": len(rule)}
                    )
                elif rule == "/":
                    rule_regex = "^" + rule + reg_str
                    match = re.match(rule_regex, path)
                    if match is not None:
                        matched_rules.append(
                            {"status": "allowed", "rule": rule, "len": len(rule)}
                        )
        return matched_rules

    @staticmethod
    def match_disallow_rules(rules: list, path: str, reg_str: str):
        """
        Match the provided path against a list of disallowed rules.

        **Inputs**

        * rules (list): A list of disallowed rules to be matched against.
        * path (str): The path to be matched against the rules.
        * reg_str (str): A regular expression string used for wildcard matching.

        **Returns**

        * list: A list of matched rules based on the path.
        """
        regex_end_with_slash = r"^(.*?)/$"
        matched_rules = []
        for rule in rules:
            if "*" in rule:
                rule_regex = f"^{rule.replace('*', '')}"
                match = re.match(rule_regex, path)
                if match is not None:
                    matched_rules.append(
                        {"status": "disallow", "rule": rule, "len": len(rule)}
                    )
            else:
                if rule == path:
                    matched_rules.append(
                        {"status": "disallow", "rule": rule, "len": len(rule)}
                    )
                elif re.match(regex_end_with_slash, rule) is not None:
                    rule_regex = f"^{rule}{reg_str}"
                    match = re.match(rule_regex, path)
                    if match is not None:
                        matched_rules.append(
                            {"status": "disallow", "rule": rule, "len": len(rule)}
                        )

        return matched_rules

    @staticmethod
    def print_result(matching_rules_list: list, path: str, user_agent: str):
        """
        Print the result of matching rules for a given path and user agent.

        **Inputs**

        * dict_rules_match (list): A list of matched rules for the path and user agent.
        * path (str): The path for which rules were matched.
        * user_agent (str): The user agent for which rules were matched.

        **Returns**

        This function doesn't return a value. It prints the result based on the matched rules.
        """
        try:
            max_len_rule = max(matching_rules_list, key=lambda x: x["len"])
            max_len = max(d["len"] for d in matching_rules_list)
            max_len_count = sum(1 for d in matching_rules_list if d["len"] == max_len)
            if max_len_count >= 2:
                return True, {
                    "status": "allowed",
                    "path": path,
                    "user_agent": user_agent,
                }
            else:
                status = max_len_rule["status"]
                if status == "allowed":
                    return True, {
                        "status": "allowed",
                        "path": path,
                        "user_agent": user_agent,
                    }
                else:
                    return False, {
                        "status": "disallow",
                        "path": path,
                        "user_agent": user_agent,
                    }
        except Exception:
            return True, {
                "status": "allowed",
                "path": path,
                "user_agent": user_agent,
                "msg": "No matching rules so it's allowed by default",
            }

    def get_crawl_delay(self, user_agent: str):
        """
        Get and print the crawl delay for a specific user-agent in the robots.txt file.

        **Inputs**

        * user_agent (str): The user-agent for which to retrieve the crawl delay.

        **Returns**

        """
        if user_agent is None:
            return False, {
                "user_agent": None,
                "crawl_delay": None,
                "msg": "Please provide a user agent",
            }
        if self._url is not None:
            crawl_block = self.parse(self._url, action="crawl_delay")
            if crawl_block is None:
                return None
            blocks = self.get_specific_block(crawl_block, user_agent)
            if blocks is not None:
                return True, {
                    "user_agent": user_agent,
                    "crawl_delay": blocks["crawl_delay"],
                }
            else:
                return False, {"user_agent": user_agent, "crawl_delay": None}


if __name__ == "__main__":
    rb = RobotParser()
    rb.set_url("https://ensimag.grenoble-inp.fr/")

    ret_rule = rb.check_for_rule("blabla", "/adminsite/")
    if ret_rule is not None:
        print(f"ret_rule: {ret_rule}")
    """
        ret_site = rb.get_sitemaps()
        print(f"ret_site: {ret_site}")

        ret_crawl = rb.get_crawl_delay("Bb")
        if ret_crawl is not None:
            print(f"ret_crawl: {ret_crawl}")"""
