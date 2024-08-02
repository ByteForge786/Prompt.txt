import re

def convert_date_format_in_sql(sql):
    def convert_date(match):
        date_str = match.group(0)
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

    # Pattern to match 'whatever.cobdate' in the SQL
    cobdate_pattern = r'\b\w+\.cobdate\b'
    
    # Pattern to match date in 'yyyymmdd' format
    date_pattern = r'\b\d{8}\b'

    # Find all occurrences of 'whatever.cobdate'
    cobdate_matches = re.findall(cobdate_pattern, sql)

    # For each match, look for adjacent date patterns and convert them
    for cobdate in cobdate_matches:
        # Look for 'between date1 and date2' pattern
        between_pattern = rf"{cobdate}\s+between\s+({date_pattern})\s+and\s+({date_pattern})"
        sql = re.sub(between_pattern, lambda m: f"{cobdate} between {convert_date(m.group(1))} and {convert_date(m.group(2))}", sql)

        # Look for 'after date' pattern
        after_pattern = rf"(?:after|>)\s*{cobdate}\s*({date_pattern})"
        sql = re.sub(after_pattern, lambda m: f"> {cobdate} {convert_date(m.group(1))}", sql)

    return sql
