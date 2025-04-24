import argparse
import logging
from typing import Optional

from ..parser.robot_parser import RobotParser

def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="RobotXT Parser - A robots.txt parser and analyzer"
    )
    
    parser.add_argument(
        "url",
        help="URL to analyze"
    )
    
    parser.add_argument(
        "--user-agent",
        "-u",
        help="User agent to check rules for",
        default="*"
    )
    
    parser.add_argument(
        "--path",
        "-p",
        help="Path to check access for",
        default="/"
    )
    
    parser.add_argument(
        "--action",
        "-a",
        choices=["crawl_delay", "sitemaps", "user_agent"],
        help="Action to perform",
        default="user_agent"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()

def main() -> Optional[int]:
    """Main entry point for the CLI."""
    args = parse_args()
    setup_logging("DEBUG" if args.verbose else "INFO")
    
    try:
        parser = RobotParser()
        parser.set_url(args.url)
        
        if args.action == "crawl_delay":
            delay = parser.get_crawl_delay(args.user_agent)
            print(f"Crawl delay for {args.user_agent}: {delay}")
            
        elif args.action == "sitemaps":
            sitemaps = parser.get_sitemaps()
            print("Sitemaps:")
            for sitemap in sitemaps:
                print(f"  - {sitemap}")
                
        elif args.action == "user_agent":
            is_allowed = parser.check_for_rule(args.user_agent, args.path)
            print(f"Path {args.path} is {'allowed' if is_allowed else 'disallowed'} "
                  f"for user-agent {args.user_agent}")
            
        return 0
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main() or 0) 