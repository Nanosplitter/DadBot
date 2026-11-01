import html
import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlencode, urlsplit, urlunsplit

import aiohttp
import requests

APOD_ENDPOINT = "https://science.nasa.gov/wp-json/wp/v2/apod-basic"
USER_AGENT = "DadBot/1.0 (Astronomy Picture of the Day)"
# Discord's base upload limit. Larger originals are linked and a smaller file is attached.
DISCORD_UPLOAD_LIMIT = 10 * 1024 * 1024


@dataclass
class ApodPost:
    title: str
    explanation: str
    media_type: str
    image_url: Optional[str]
    full_image_url: Optional[str]
    link_url: Optional[str]
    date: str


def html_to_discord(raw: str) -> str:
    def link(match: re.Match) -> str:
        label = re.sub(r"<[^>]+>", "", match.group(2))
        label = html.unescape(label).strip()
        href = html.unescape(match.group(1)).strip()
        if not label or label == href or label.startswith("http://") or label.startswith("https://"):
            return ""
        return label

    text = re.sub(
        r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        link,
        raw or "",
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r"^\s*Explanation:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _without_query(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def full_size_url(hdurl: str) -> str:
    """Original asset. The feed's hdurl is a resized dynamicimage rendition."""
    parts = urlsplit(hdurl)
    path = parts.path.replace("/dynamicimage/assets/", "/content/dam/", 1)
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def _scaled_url(url: str, width: int) -> str:
    parts = urlsplit(url)
    path = parts.path.replace("/content/dam/", "/dynamicimage/assets/", 1)
    if "/dynamicimage/" not in path:
        path = "/dynamicimage" + path
    return urlunsplit(
        (parts.scheme, parts.netloc, path, urlencode({"w": str(width), "fit": "clip"}), "")
    )


def _image_filename(url: str, content_type: str) -> str:
    content_type = (content_type or "").lower()
    if "png" in content_type:
        return "apod.png"
    if "webp" in content_type:
        return "apod.webp"
    if "gif" in content_type:
        return "apod.gif"
    path = urlsplit(url).path.lower()
    for extension in (".png", ".webp", ".gif", ".jpg", ".jpeg"):
        if path.endswith(extension):
            return "apod" + extension.replace(".jpeg", ".jpg")
    return "apod.jpg"


def _is_real_image(url: str) -> bool:
    if not url or "nasa-logo" in url:
        return False
    try:
        response = requests.head(
            url,
            timeout=20,
            allow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        )
    except requests.RequestException:
        return False
    content_type = response.headers.get("Content-Type", "")
    return response.status_code == 200 and content_type.lower().startswith("image/")


def fetch_apod() -> Optional[ApodPost]:
    """Latest APOD from NASA's current feed.

    api.nasa.gov/planetary/apod now returns the site logo and the title
    "NASA Science". The WordPress feed still has the real title, explanation,
    and image.
    """
    try:
        response = requests.get(
            APOD_ENDPOINT,
            params={"per_page": 1},
            timeout=30,
            headers={"User-Agent": USER_AGENT},
        )
    except requests.RequestException:
        return None

    item = None
    try:
        body = response.json()
        if isinstance(body, list) and body and isinstance(body[0], dict):
            item = body[0]
    except Exception:
        item = None

    if response.status_code != 200 or item is None:
        return None

    hdurl = item.get("hdurl") or ""
    if "nasa-logo" in hdurl:
        hdurl = ""

    full_image = ""
    image_url = ""
    if item.get("media_type") == "image" and hdurl:
        candidate = full_size_url(hdurl)
        if _is_real_image(candidate):
            full_image = candidate
        else:
            full_image = _without_query(hdurl)
        image_url = full_image

    return ApodPost(
        title=str(item.get("title") or "Astronomy Picture of the Day"),
        explanation=html_to_discord(str(item.get("explanation") or "")),
        media_type=str(item.get("media_type") or ""),
        image_url=image_url or None,
        full_image_url=full_image or None,
        link_url=item.get("permalink") or item.get("url"),
        date=str(item.get("date") or ""),
    )


def format_apod_message(post: ApodPost, suffix: str = "") -> str:
    header = f"# APOD - {post.title}\n"
    if post.full_image_url:
        header += f"Full size: <{post.full_image_url}>\n"
    footer = f"\n{suffix}" if suffix else ""
    text = header + f">>> {post.explanation}" + footer
    if len(text) <= 2000:
        return text
    budget = 2000 - len(header) - len(footer) - len(">>> ...")
    explanation = post.explanation[: max(budget, 0)].rstrip() + "..."
    return (header + f">>> {explanation}" + footer)[:2000]


async def _read_image(
    session: aiohttp.ClientSession, url: str, max_bytes: Optional[int] = None
) -> Optional[tuple[bytes, str]]:
    async with session.get(url) as resp:
        if resp.status != 200:
            return None
        content_type = resp.headers.get("Content-Type", "")
        if not content_type.lower().startswith("image/") or "nasa-logo" in url:
            return None
        if max_bytes and resp.content_length and resp.content_length > max_bytes:
            return None
        data = await resp.read()
        if not data or (max_bytes and len(data) > max_bytes):
            return None
        return data, _image_filename(url, content_type)


async def download_image(post: ApodPost) -> Optional[tuple[bytes, str]]:
    if not post.image_url and not post.full_image_url:
        return None

    candidates = []
    for url in (post.full_image_url, post.image_url):
        if url and url not in candidates:
            candidates.append(url)
    if post.full_image_url:
        for width in (4096, 2560, 1600):
            scaled = _scaled_url(post.full_image_url, width)
            if scaled not in candidates:
                candidates.append(scaled)

    try:
        async with aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as session:
            too_big = None
            for index, url in enumerate(candidates):
                is_last = index == len(candidates) - 1
                downloaded = await _read_image(
                    session, url, None if is_last else DISCORD_UPLOAD_LIMIT
                )
                if downloaded is None:
                    continue
                data, filename = downloaded
                if len(data) <= DISCORD_UPLOAD_LIMIT:
                    return data, filename
                too_big = (data, filename)
            return too_big
    except Exception:
        return None
