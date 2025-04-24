#!/usr/bin/env python3
"""
Basic example of using the RobotXT Parser.
"""

from src.robotxt_parser import RobotParser

def main():
    # Initialize the parser
    parser = RobotParser()
    
    # Set the URL to analyze
    url = "https://www.example.com"
    parser.set_url(url)
    
    # Check if a path is allowed for a specific user-agent
    user_agent = "MyBot"
    path = "/some/path"
    
    is_allowed = parser.check_for_rule(user_agent, path)
    print(f"Path {path} is {'allowed' if is_allowed else 'disallowed'} for {user_agent}")
    
    # Get all sitemaps
    sitemaps = parser.get_sitemaps()
    print("\nSitemaps:")
    for sitemap in sitemaps:
        print(f"  - {sitemap}")
    
    # Get crawl delay for a user-agent
    delay = parser.get_crawl_delay(user_agent)
    print(f"\nCrawl delay for {user_agent}: {delay}")
    
    # Parse user-agent rules
    rules = parser.parse(url, "user_agent")
    print("\nUser-agent rules:")
    for rule in rules:
        for agent, data in rule.items():
            print(f"\n{agent}:")
            print("  Allowed paths:")
            for path in data["allowed"]:
                print(f"    - {path}")
            print("  Disallowed paths:")
            for path in data["disallowed"]:
                print(f"    - {path}")

if __name__ == "__main__":
    main() 