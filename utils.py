import re


# def extract_sql(response):
#     match = re.search(r"```sql\s+(.*?)\s+```", response, re.DOTALL | re.IGNORECASE)
#     return match.group(1) if match else None


def extract_sql(response):
    matches = re.findall(r"```sql\s+(.*?)\s+```", response, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[0].strip()
    return None


def is_sql(response):
    return bool(re.search(r"```sql\s+.*?```", response, re.DOTALL | re.IGNORECASE))
