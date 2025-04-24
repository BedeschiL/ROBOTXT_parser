import pytest
from src.robotxt_parser.parser.robot_parser import RobotParser
from src.robotxt_parser.parser.exceptions import RobotException

def test_robot_parser_initialization():
    parser = RobotParser()
    assert parser.url == ""
    assert parser.robot_content is None

def test_set_url():
    parser = RobotParser()
    parser.set_url("https://example.com")
    assert parser.url == "https://example.com"

def test_invalid_url():
    parser = RobotParser()
    with pytest.raises(RobotException):
        parser.set_url(None)
    
    with pytest.raises(RobotException):
        parser.set_url("")
        
    with pytest.raises(RobotException):
        parser.set_url(123)  # type: ignore

def test_parse_crawl_delay():
    parser = RobotParser()
    parser.robot_content = """
    User-agent: *
    Crawl-delay: 10
    
    User-agent: googlebot
    Crawl-delay: 5
    """
    result = parser.parse("https://example.com", "crawl_delay")
    assert result["*"]["crawl_delay"] == "10"
    assert result["googlebot"]["crawl_delay"] == "5"

def test_parse_sitemaps():
    parser = RobotParser()
    parser.robot_content = """
    Sitemap: https://example.com/sitemap.xml
    Sitemap: https://example.com/sitemap-images.xml
    """
    result = parser.parse("https://example.com", "sitemaps")
    assert isinstance(result, list)
    assert len(result) == 2
    assert "https://example.com/sitemap.xml" in result
    assert "https://example.com/sitemap-images.xml" in result

def test_parse_user_agent():
    parser = RobotParser()
    parser.robot_content = """
    User-agent: *
    Allow: /public/
    Disallow: /private/
    
    User-agent: Googlebot
    Allow: /images/
    Disallow: /admin/
    """
    result = parser.parse("https://example.com", "user_agent")
    assert len(result) == 2
    assert result[0]["*"]["allowed"] == ["/public/"]
    assert result[0]["*"]["disallowed"] == ["/private/"]
    assert result[1]["googlebot"]["allowed"] == ["/images/"]
    assert result[1]["googlebot"]["disallowed"] == ["/admin/"]

def test_check_for_rule():
    parser = RobotParser()
    parser.robot_content = """
    User-agent: *
    Allow: /public/
    Disallow: /private/
    """
    assert parser.check_for_rule("*", "/public/page.html") is True
    assert parser.check_for_rule("*", "/private/page.html") is False
    assert parser.check_for_rule("*", "/other/page.html") is True

def test_get_crawl_delay():
    parser = RobotParser()
    parser.robot_content = """
    User-agent: *
    Crawl-delay: 10
    """
    assert parser.get_crawl_delay("*") == 10.0
    assert parser.get_crawl_delay("Googlebot") is None 