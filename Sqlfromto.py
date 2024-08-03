import re
def convert_date_format_in_sql(sql):
    def convert_date(date_str):
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    # Pattern to match 'whatever.cobdate' in the SQL (case insensitive)
    cobdate_pattern = r'\b\w+\.cobdate\b'
    
    # Pattern to match date in 'yyyymmdd' format
    date_pattern = r'\b\d{8}\b'
    # Find all occurrences of 'whatever.cobdate'
    cobdate_matches = re.findall(cobdate_pattern, sql, re.IGNORECASE)
    # For each match, look for adjacent date patterns and convert them
    for cobdate in cobdate_matches:
        # Look for 'between date1 and date2' pattern (case insensitive)
        between_pattern = rf"({cobdate})\s+(?i:between)\s+({date_pattern})\s+(?i:and)\s+({date_pattern})"
        sql = re.sub(between_pattern, lambda m: f"{m.group(1)} BETWEEN {convert_date(m.group(2))} AND {convert_date(m.group(3))}", sql, flags=re.IGNORECASE)
        # Look for comparison operators (case insensitive)
        comparison_pattern = rf"({cobdate}\s*[><]=?\s*)({date_pattern})"
        sql = re.sub(comparison_pattern, lambda m: f"{m.group(1)}{convert_date(m.group(2))}", sql, flags=re.IGNORECASE)
    return sql
Some examples didn't work like cobdate between 20240731 AND 20240831, cobdate >= 20240601, is it case sensitivity issue or what is the issue check and give correct code

import re

def convert_date_format_in_sql(sql):
    def convert_date(date_str):
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    
    # Pattern to match 'whatever.cobdate' or just 'cobdate' in the SQL (case insensitive)
    cobdate_pattern = r'\b(?:\w+\.)?cobdate\b'
    
    # Pattern to match date in 'yyyymmdd' format
    date_pattern = r'\b\d{8}\b'
    
    # Find all occurrences of 'whatever.cobdate' or 'cobdate'
    cobdate_matches = re.findall(cobdate_pattern, sql, re.IGNORECASE)
    
    # For each match, look for adjacent date patterns and convert them
    for cobdate in cobdate_matches:
        # Look for 'between date1 and date2' pattern (case insensitive)
        between_pattern = rf"({cobdate})\s+(?i:between)\s+({date_pattern})\s+(?i:and)\s+({date_pattern})"
        sql = re.sub(between_pattern, lambda m: f"{m.group(1)} BETWEEN {convert_date(m.group(2))} AND {convert_date(m.group(3))}", sql, flags=re.IGNORECASE)
        
        # Look for comparison operators (case insensitive)
        comparison_pattern = rf"({cobdate}\s*[><]=?\s*)({date_pattern})"
        sql = re.sub(comparison_pattern, lambda m: f"{m.group(1)}{convert_date(m.group(2))}", sql, flags=re.IGNORECASE)
    
    return sql





import re

def convert_date_format_in_sql(sql):
    def convert_date(date_str):
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

    # Pattern to match 'whatever.cobdate' in the SQL (case insensitive)
    cobdate_pattern = r'\b\w+\.cobdate\b'
    
    # Pattern to match date in 'yyyymmdd' format
    date_pattern = r'\b\d{8}\b'

    # Find all occurrences of 'whatever.cobdate'
    cobdate_matches = re.findall(cobdate_pattern, sql, re.IGNORECASE)

    # For each match, look for adjacent date patterns and convert them
    for cobdate in cobdate_matches:
        # Create a case-insensitive pattern for this specific cobdate
        cobdate_ci = ''.join(f'[{c.lower()}{c.upper()}]' for c in cobdate)

        # Look for 'between date1 and date2' pattern (case insensitive)
        between_pattern = rf"({cobdate_ci})\s+(?:between)\s+({date_pattern})\s+(?:and)\s+({date_pattern})"
        sql = re.sub(between_pattern, lambda m: f"{m.group(1)} BETWEEN {convert_date(m.group(2))} AND {convert_date(m.group(3))}", sql)
        
        # Look for comparison operators (case insensitive)
        comparison_pattern = rf"({cobdate_ci})\s*([><]=?|=)\s*({date_pattern})"
        sql = re.sub(comparison_pattern, lambda m: f"{m.group(1)} {m.group(2)} {convert_date(m.group(3))}", sql)

    return sql
