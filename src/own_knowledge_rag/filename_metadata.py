"""Extract structured metadata from corpus filenames.

Filenames in this corpus follow a stable pattern:
    {country_name_parts}_{iso_code}.{ext}   → locale_profile
    all_twilio_sms_guidelines_index.*        → index
    all_twilio_sms_guidelines.*              → aggregate
    anything_else.*                          → general

This extraction happens before content parsing — zero I/O cost.
"""

import re
from dataclasses import dataclass
from pathlib import Path

# Full ISO-2 → region mapping for the corpus
_ISO_TO_REGION: dict[str, str] = {
    "AF": "Asia", "AL": "Europe", "DZ": "Africa", "AS": "Oceania",
    "AD": "Europe", "AO": "Africa", "AI": "Americas", "AG": "Americas",
    "AR": "Americas", "AM": "Asia", "AW": "Americas", "AU": "Oceania",
    "AT": "Europe", "AZ": "Asia", "BS": "Americas", "BH": "Asia",
    "BD": "Asia", "BB": "Americas", "BY": "Europe", "BE": "Europe",
    "BZ": "Americas", "BJ": "Africa", "BM": "Americas", "BT": "Asia",
    "BO": "Americas", "BA": "Europe", "BW": "Africa", "BR": "Americas",
    "VG": "Americas", "BN": "Asia", "BG": "Europe", "BF": "Africa",
    "BI": "Africa", "KH": "Asia", "CM": "Africa", "CA": "Americas",
    "CV": "Africa", "KY": "Americas", "CF": "Africa", "TD": "Africa",
    "CL": "Americas", "CN": "Asia", "CO": "Americas", "KM": "Africa",
    "CK": "Oceania", "CR": "Americas", "HR": "Europe", "CU": "Americas",
    "CY": "Europe", "CZ": "Europe", "CD": "Africa", "DK": "Europe",
    "DJ": "Africa", "DM": "Americas", "DO": "Americas", "EC": "Americas",
    "EG": "Africa", "SV": "Americas", "GQ": "Africa", "ER": "Africa",
    "EE": "Europe", "ET": "Africa", "FO": "Europe", "FJ": "Oceania",
    "FI": "Europe", "FR": "Europe", "GF": "Americas", "PF": "Oceania",
    "GA": "Africa", "GM": "Africa", "GE": "Asia", "DE": "Europe",
    "GH": "Africa", "GI": "Europe", "GR": "Europe", "GL": "Americas",
    "GD": "Americas", "GP": "Americas", "GU": "Oceania", "GT": "Americas",
    "GG": "Europe", "GW": "Africa", "GN": "Africa", "GY": "Americas",
    "HT": "Americas", "HN": "Americas", "HK": "Asia", "HU": "Europe",
    "IS": "Europe", "IN": "Asia", "ID": "Asia", "IR": "Asia",
    "IQ": "Asia", "IE": "Europe", "IL": "Asia", "IT": "Europe",
    "CI": "Africa", "JM": "Americas", "JP": "Asia", "JE": "Europe",
    "JO": "Asia", "KZ": "Asia", "KE": "Africa", "XK": "Europe",
    "KI": "Oceania", "KW": "Asia", "KG": "Asia", "LA": "Asia", "LV": "Europe",
    "LB": "Asia", "LS": "Africa", "LR": "Africa", "LY": "Africa",
    "LI": "Europe", "LT": "Europe", "LU": "Europe", "MO": "Asia",
    "MK": "Europe", "MG": "Africa", "MW": "Africa", "MY": "Asia",
    "MV": "Asia", "ML": "Africa", "MT": "Europe", "MH": "Oceania",
    "MQ": "Americas", "MR": "Africa", "MU": "Africa", "MX": "Americas",
    "MD": "Europe", "MC": "Europe", "MN": "Asia", "ME": "Europe",
    "MS": "Americas", "MA": "Africa", "MZ": "Africa", "MM": "Asia",
    "NA": "Africa", "NP": "Asia", "AN": "Americas", "NL": "Europe",
    "NC": "Oceania", "NZ": "Oceania", "NI": "Americas", "NE": "Africa",
    "NG": "Africa", "NU": "Oceania", "NF": "Oceania", "NO": "Europe",
    "OM": "Asia", "PK": "Asia", "PW": "Oceania", "PS": "Asia",
    "PA": "Americas", "PG": "Oceania", "PY": "Americas", "PE": "Americas",
    "PH": "Asia", "PL": "Europe", "PT": "Europe", "PR": "Americas",
    "QA": "Asia", "RE": "Africa", "CG": "Africa", "RO": "Europe",
    "RU": "Europe", "RW": "Africa", "LC": "Americas", "VC": "Americas",
    "WS": "Oceania", "SM": "Europe", "ST": "Africa", "SA": "Asia",
    "SN": "Africa", "RS": "Europe", "SC": "Africa", "SL": "Africa",
    "SG": "Asia", "SK": "Europe", "SI": "Europe", "SB": "Oceania",
    "SO": "Africa", "ZA": "Africa", "KR": "Asia", "SS": "Africa",
    "ES": "Europe", "LK": "Asia", "KN": "Americas", "PM": "Americas",
    "SD": "Africa", "SR": "Americas", "SZ": "Africa", "SE": "Europe",
    "CH": "Europe", "SY": "Asia", "TW": "Asia", "TJ": "Asia",
    "TZ": "Africa", "TH": "Asia", "TL": "Asia", "TG": "Africa",
    "TO": "Oceania", "TT": "Americas", "TN": "Africa", "TR": "Europe",
    "TM": "Asia", "TC": "Americas", "TV": "Oceania", "UG": "Africa",
    "UA": "Europe", "AE": "Asia", "GB": "Europe", "US": "Americas",
    "VI": "Americas", "UY": "Americas", "UZ": "Asia", "VU": "Oceania",
    "VE": "Americas", "VN": "Asia", "YE": "Asia", "ZM": "Africa",
    "ZW": "Africa",
}

# Common country name → ISO-2 mapping for fallback detection
_COUNTRY_TO_ISO: dict[str, str] = {
    "spain": "ES", "vietnam": "VN", "algeria": "DZ", "germany": "DE",
    "france": "FR", "italy": "IT", "united_kingdom": "GB", "uk": "GB",
    "united_states": "US", "usa": "US", "brazil": "BR", "india": "IN",
    "china": "CN", "japan": "JP", "canada": "CA", "australia": "AU",
}

# MCC → ISO mapping for the corpus countries
_MCC_TO_ISO: dict[str, str] = {
    "214": "ES", "452": "VN", "603": "DZ", "525": "LA", "262": "DE",
    "208": "FR", "234": "GB", "310": "US", "311": "US", "440": "JP",
    "441": "JP", "505": "AU", "724": "BR", "204": "NL",
}

# ISO → Country Name for canonical display
_ISO_TO_COUNTRY: dict[str, str] = {
    "ES": "Spain", "VN": "Vietnam", "DZ": "Algeria", "LA": "Laos",
    "DE": "Germany", "FR": "France", "GB": "United Kingdom", "US": "United States",
    "JP": "Japan", "AU": "Australia", "BR": "Brazil", "NL": "Netherlands",
    "KI": "Kiribati",
}

# Country names we can reconstruct that differ from naive title-casing
_COUNTRY_NAME_OVERRIDES: dict[str, str] = {
    "r_union_france_re": "Réunion",
    "cote_d_ivoire_ci": "Côte d'Ivoire",
}


@dataclass(frozen=True)
class FilenameMetadata:
    country: str       # "Spain" — human readable display name
    iso_code: str      # "ES" — uppercase 2-letter ISO code (empty for non-locale files)
    region: str        # "Europe" (empty for non-locale files)
    corpus_type: str   # "locale_profile" | "index" | "aggregate" | "general"


_EMPTY = FilenameMetadata(country="", iso_code="", region="", corpus_type="general")


def extract_filename_metadata(path: Path) -> FilenameMetadata:
    """Derive structured metadata from a corpus filename without reading file content."""
    stem = path.stem.lower().replace("-", "_")

    # Check override table first
    if stem in _COUNTRY_NAME_OVERRIDES:
        parts = stem.split("_")
        iso_code = parts[-1].upper()
        return FilenameMetadata(
            country=_COUNTRY_NAME_OVERRIDES[stem],
            iso_code=iso_code,
            region=_ISO_TO_REGION.get(iso_code, ""),
            corpus_type="locale_profile",
        )

    # Index / aggregate files
    if "guidelines_index" in stem or stem.endswith("_index"):
        return FilenameMetadata(country="", iso_code="", region="", corpus_type="index")
    if stem.startswith("all_") or "guidelines" in stem:
        return FilenameMetadata(country="", iso_code="", region="", corpus_type="aggregate")

    parts = stem.split("_")
    if len(parts) < 2:
        return _EMPTY

    last = parts[-1]
    # Locale profile: last segment is exactly 2 alphabetic chars
    if len(last) == 2 and last.isalpha():
        iso_code = last.upper()
        # Country name: everything before the last segment, skip 2-char territory
        # qualifiers like _uk_ in bermuda_uk_bm
        country_parts = [
            p for p in parts[:-1]
            if not (len(p) == 2 and p.isalpha())
        ]
        if not country_parts:
            country_parts = parts[:-1]
        country = " ".join(p.capitalize() for p in country_parts)
        region = _ISO_TO_REGION.get(iso_code, "")
        return FilenameMetadata(
            country=country,
            iso_code=iso_code,
            region=region,
            corpus_type="locale_profile",
        )

    # Fallback: scan all parts for a known country name, ISO, or MCC
    # This handles legacy filenames like Spain__2014.md (where 214 is the MCC)
    for part in parts:
        part_clean = part.strip()
        
        # Check for 3-digit MCC anywhere in the part (e.g. "214" in "2014" or "__214")
        mcc_match = re.search(r"\b(214|452|603|525|262|208|234|310|311|440|441|505|724|204)\b", part_clean)
        if mcc_match:
            mcc = mcc_match.group(1)
            iso = _MCC_TO_ISO.get(mcc)
            if iso:
                return FilenameMetadata(
                    country=_ISO_TO_COUNTRY.get(iso, ""),
                    iso_code=iso,
                    region=_ISO_TO_REGION.get(iso, ""),
                    corpus_type="locale_profile",
                )

        # Heuristic: if a part is a known country name or ISO
        for name, iso in _COUNTRY_TO_ISO.items():
            if name == part_clean or part_clean.startswith(name + "_") or part_clean.endswith("_" + name):
                return FilenameMetadata(
                    country=name.capitalize(),
                    iso_code=iso,
                    region=_ISO_TO_REGION.get(iso, ""),
                    corpus_type="locale_profile",
                )
        
        part_upper = part_clean.upper()
        if len(part_upper) == 2 and part_upper in _ISO_TO_REGION:
            return FilenameMetadata(
                country="", # Unknown name, but we have the ISO
                iso_code=part_upper,
                region=_ISO_TO_REGION.get(part_upper, ""),
                corpus_type="locale_profile",
            )

    return _EMPTY


def build_country_index(iso_to_region: dict[str, str] | None = None) -> dict[str, str]:
    """Return a lowercase country-name → ISO-code reverse map built from filenames.

    Callers can augment this with tags found in already-indexed blocks via
    `augment_country_index_from_blocks`.
    """
    index: dict[str, str] = {}
    # Build from the known ISO table — one entry per ISO code
    for iso, _region in _ISO_TO_REGION.items():
        index[iso.lower()] = iso  # "es" → "ES"
    for name, iso in _COUNTRY_TO_ISO.items():
        index[name.replace("_", " ")] = iso
        index[name] = iso
    for iso, country in _ISO_TO_COUNTRY.items():
        index[country.lower()] = iso
    return index


def augment_country_index(index: dict[str, str], country: str, iso_code: str) -> None:
    """Add a country name → iso_code entry (and common aliases) to the index."""
    if not country or not iso_code:
        return
    key = country.strip().lower()
    if key:
        index[key] = iso_code
    # Also index individual words of multi-word names (e.g. "united states" → "United States")
    words = key.split()
    if len(words) > 1:
        for word in words:
            if len(word) > 3 and word not in {"islands", "republic", "democratic", "south", "north"}:
                index.setdefault(word, iso_code)
