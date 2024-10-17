import hashlib
from browserforge.fingerprints import FingerprintGenerator
from PIL import Image, ImageDraw, ImageFont
import random
import io
import json

def hash_value(value):
    return hashlib.md5(value.encode() if isinstance(value, str) else value).hexdigest()

def _device_name(fingerprint):
    ua_data = fingerprint.navigator.userAgentData
    brand = ua_data['brands'][0]['brand']
    version = ua_data['brands'][0]['version']
    platform = ua_data['platform']
    return f"{brand} {version} on {platform}"

def _webgl_fingerprint(video_card):
    return hash_value(f"{video_card.renderer}::{video_card.vendor}")

def _canvas_fingerprint():
    image = Image.new("RGB", (200, 50), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle([10, 10, 160, 40], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    draw.text((10, 40), "Canvas Fingerprint Test", fill=(0, 0, 0), font=ImageFont.load_default())
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return hash_value(img_byte_arr.getvalue())

fingerprint_data = FingerprintGenerator().generate()

print(json.dumps({
    "fp": {
        "user_agent": hash_value(fingerprint_data.navigator.userAgent),
        "language": fingerprint_data.navigator.language,
        "pixel_ratio": fingerprint_data.screen.devicePixelRatio,
        "timezone_offset": fingerprint_data.navigator.extraProperties.get('timezoneOffset', 'unknown'),
        "session_storage": 1,
        "local_storage": 1,
        "indexed_db": 1,
        "open_database": 0,
        "cpu_class": "unknown",
        "navigator_platform": fingerprint_data.navigator.platform,
        "do_not_track": fingerprint_data.navigator.doNotTrack or "unknown",
        "regular_plugins": hash_value(";".join([p['name'] for p in fingerprint_data.pluginsData['plugins']])),
        "canvas": _canvas_fingerprint(),
        "webgl": _webgl_fingerprint(fingerprint_data.videoCard),
        "adblock": False,
        "has_lied_os": fingerprint_data.navigator.platform != fingerprint_data.navigator.platform,
        "touch_support": "0;false;false",
        "device_name": _device_name(fingerprint_data),
        "js_fonts": hash_value(";".join(fingerprint_data.fonts))
    }
}))
