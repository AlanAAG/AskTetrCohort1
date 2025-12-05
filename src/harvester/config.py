"""
Selenium-oriented configuration for the harvester module.

This converts prior Playwright selectors into robust Selenium-friendly
XPaths/CSS selectors and keeps course mappings and URLs separated from logic.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices
from selenium.webdriver.common.by import By
import os

# --- Core URLs ---
LOGIN_URL = "https://coach.tetr.com/login"
BASE_URL = "https://coach.tetr.com/"
COURSES_URL = BASE_URL + "courses"

# File path to persist cookies/session if desired (used by Selenium helpers)
AUTH_STATE_FILE = "data/auth_state.json"

# --- Login Page Selectors (Selenium) ---
# Prioritized selector lists to support resilient fallbacks.
USERNAME_SELECTORS = [
    (By.XPATH, "//input[@placeholder='Enter Your Email ID']"),
    (By.XPATH, "//input[@name='officialEmail']"),
]

PASSWORD_SELECTORS = [
    (By.XPATH, "//input[@placeholder='Enter Your Password']"),
    (By.XPATH, "//input[@name='password']"),
]

LOGIN_BUTTON_SELECTORS = [
    (By.XPATH, "//button[normalize-space(.)='Login']"),
    (By.XPATH, "//button[normalize-space(.)='Sign In']"),
    (By.XPATH, "//button[@type='submit']"),
]

# A generic indicator that we are not on the login page anymore
DASHBOARD_INDICATOR_CSS = '#gtm-IdDashboard'

# --- Courses Page (Selenium) ---
# Group header: div.domainHeader containing p.title == {group_name}
GROUP_HEADER_XPATH_TEMPLATE = "//p[contains(@class, 'title') and normalize-space(.)='{group_name}']/ancestor::div[contains(@class, 'domainHeader')][1]"

# Course link: Div containing the course code span (Cohort 1 structure has no anchor tag)
COURSE_LINK_XPATH_TEMPLATE = "//span[contains(@class, 'pIdName') and normalize-space(.)='{course_code}']/ancestor::div[contains(@class, 'sc-eDWCr')][1]"

# Fallback course card container (handles layouts where program code sits inside divs under anchor wrappers)
COURSE_CARD_FALLBACK_XPATH_TEMPLATE = (
    "//span[contains(concat(' ', normalize-space(@class), ' '), ' pIdName ') and normalize-space(.)='{course_code}']"
    "/ancestor::div[contains(@class, 'sc-eDWCr') or contains(@class, 'domainCourses')][1]"
)

# --- Course Details Page (Resources Tab Navigation) ---
RESOURCES_TAB_SELECTORS = [
    (
        By.XPATH,
        "//div[.//img[contains(@src, 'resources.svg')] and .//p[normalize-space(.)='Resources']]",
    ),
    (
        By.XPATH,
        "//p[normalize-space(.)='Resources']/ancestor::div[contains(@class, 'sc-kMjNwy')][1]",
    ),
    (
        By.XPATH,
        "//p[normalize-space(.)='Resources']/ancestor::li[1]",
    ),
    (
        By.XPATH,
        "//h4[normalize-space(.)='Resources']",
    ),
]

# Section headers inside resources
SECTION_HEADER_XPATH_TPL = "//p[contains(@class, 'name') and normalize-space(.)='{section_title}']"

PRE_READ_SECTION_TITLE = "Pre-Read Materials"
IN_CLASS_SECTION_TITLE = "In Class Materials"
POST_CLASS_SECTION_TITLE = "Post Class Materials"
SESSION_RECORDINGS_SECTION_TITLE = "Session Recordings"

# Resource items and sub-elements
RESOURCE_ITEM_CSS = "div.fileBox"
RESOURCE_TITLE_CSS = "div.fileContentCol p"
RESOURCE_DATE_CSS = "div.fileContentCol span"

# --- Transcript Scraping Selectors ---
# Google Drive Web Viewer
DRIVE_PLAY_BUTTON_CSS = "button[jsname='IGlMSc'], button[jsname='dW8tsb']"
DRIVE_SETTINGS_BUTTON_CSS = "button[jsname='dq27Te'], button[jsname='J7HKb']"
DRIVE_TRANSCRIPT_HEADING_CSS = "h2#ucc-0"
DRIVE_TRANSCRIPT_CONTAINER_CSS = "div[jsname='h7hTqc']"
DRIVE_TRANSCRIPT_SEGMENT_CSS = "div.JnEIz div.wyBDIb, div[jsname='h7hTqc'] div.wyBDIb"

# Zoom Web Viewer
ZOOM_TRANSCRIPT_CONTAINER_CSS = "div.transcript-container"
ZOOM_TRANSCRIPT_LIST_CSS = "ul.transcript-list"
ZOOM_TRANSCRIPT_TEXT_CSS = "div.timeline div.text"

# Initial interaction targets (best-effort)
ZOOM_INITIAL_INTERACTIONS = [
    "video",
    "div.player-container",
    "div#player",
    "div.playback-video",
    "canvas",
]

# --- Course Mappings ---

# Updated for Cohort 1
COURSE_MAP = {
    # Group: Entrepreneurship, Innovation and Design
    "CRBL101": {"name": "CRBL101", "group": "Entrepreneurship, Innovation and Design", "code": "CRBL101", "full_name": "CRBL101"},
    "FIFI103": {"name": "FIFI103", "group": "Entrepreneurship, Innovation and Design", "code": "FIFI103", "full_name": "FIFI103"},
    "FIFI104": {"name": "FIFI104", "group": "Entrepreneurship, Innovation and Design", "code": "FIFI104", "full_name": "FIFI104"},
    "LEIP101": {"name": "LEIP101", "group": "Entrepreneurship, Innovation and Design", "code": "LEIP101", "full_name": "LEIP101"},
    "PRTC204": {"name": "PRTC204", "group": "Entrepreneurship, Innovation and Design", "code": "PRTC204", "full_name": "PRTC204"},

    # Group: Management Project - III
    "CAP023": {"name": "CAP023", "group": "Management Project - III", "code": "CAP023", "full_name": "CAP023"},
    "CAP024": {"name": "CAP024", "group": "Management Project - III", "code": "CAP024", "full_name": "CAP024"},
    "CAP025": {"name": "CAP025", "group": "Management Project - III", "code": "CAP025", "full_name": "CAP025"},
    "CAP301": {"name": "CAP301", "group": "Management Project - III", "code": "CAP301", "full_name": "CAP301"},
    "COMM203": {"name": "COMM203", "group": "Management Project - III", "code": "COMM203", "full_name": "COMM203"},
    "STC101": {"name": "STC101", "group": "Management Project - III", "code": "STC101", "full_name": "STC101"},

    # Group: Management Strategy
    "MAST204": {"name": "MAST204", "group": "Management Strategy", "code": "MAST204", "full_name": "MAST204"},
    "MAST205": {"name": "MAST205", "group": "Management Strategy", "code": "MAST205", "full_name": "MAST205"},

    # Group: Global Dynamics
    "LA103": {"name": "LA103", "group": "Global Dynamics", "code": "LA103", "full_name": "LA103"},
    "MAST103": {"name": "MAST103", "group": "Global Dynamics", "code": "MAST103", "full_name": "MAST103"},

    # Group: Market Research
    "SAMA103": {"name": "SAMA103", "group": "Market Research", "code": "SAMA103", "full_name": "SAMA103"},
}

# Default visible courses (from partner script)
# Updating to empty or safe default as previous defaults might not exist
DEFAULT_VISIBLE_COURSES = set()

# --- Other Settings ---
# Cutoff date logic handled dynamically in the pipeline


# --- Structured settings (via Pydantic Settings) ---
class HarvesterSettings(BaseSettings):
    """Centralized, typed settings for harvester behavior.

    Values can be configured via environment variables. Prefer the
    HARVESTER_* variants, but common legacy envs are supported where noted.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore undeclared env vars (e.g., GEMINI_API_KEY)
    )

    # Accept both HARVESTER_SELENIUM_HEADLESS and legacy SELENIUM_HEADLESS
    selenium_headless: bool = Field(
        default=True,
        validation_alias=AliasChoices("HARVESTER_SELENIUM_HEADLESS", "SELENIUM_HEADLESS"),
    )

    # Page load timeout for Selenium's driver
    page_load_timeout: int = Field(
        default=60,
        validation_alias=AliasChoices("HARVESTER_PAGE_LOAD_TIMEOUT"),
    )

    # Default wait timeout for WebDriverWait operations
    wait_timeout: int = Field(
        default=30,
        validation_alias=AliasChoices("HARVESTER_WAIT_TIMEOUT"),
    )

    # Directory to store screenshots when errors occur
    screenshot_dir: str = Field(
        default="logs/error_screenshots",
        validation_alias=AliasChoices("HARVESTER_SCREENSHOT_DIR"),
    )

    # Temporary downloads directory for any saved assets
    downloads_dir: str = Field(
        default="/tmp/harvester_downloads",
        validation_alias=AliasChoices("HARVESTER_DOWNLOADS_DIR"),
    )
    
    # Batch size for processing resources in the main pipeline to save memory
    resource_batch_size: int = Field(
        default=50,
        validation_alias=AliasChoices("HARVESTER_RESOURCE_BATCH_SIZE"),
    )

    # --- Monitoring & Telemetry Settings ---
    telemetry_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("HARVESTER_TELEMETRY_ENABLED", "TELEMETRY_ENABLED"),
    )

    telemetry_log_level: str = Field(
        default="INFO",
        validation_alias=AliasChoices("HARVESTER_TELEMETRY_LOG_LEVEL", "TELEMETRY_LOG_LEVEL"),
    )

    # Where to persist the last pipeline status JSON
    metrics_report_path: str = Field(
        default="data/pipeline_status.json",
        validation_alias=AliasChoices("HARVESTER_METRICS_REPORT_PATH", "METRICS_REPORT_PATH"),
    )


# Instantiate settings once for module-level access
SETTINGS = HarvesterSettings()