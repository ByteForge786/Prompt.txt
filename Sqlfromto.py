import re

def convert_date_format_in_sql(sql):
    def convert_date(date_str):
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

        # Look for comparison operators
        comparison_pattern = rf"({cobdate}\s*[><]=?\s*)({date_pattern})"
        sql = re.sub(comparison_pattern, lambda m: f"{m.group(1)}{convert_date(m.group(2))}", sql)

    return sql

# Test function
def test_convert_date_format_in_sql():
    test_cases = [
        # Between case
        ("SELECT * FROM table WHERE xyz.cobdate between 20240101 and 20241231",
         "SELECT * FROM table WHERE xyz.cobdate between 2024-01-01 and 2024-12-31"),
        
        # Greater than case
        ("SELECT * FROM table WHERE e.cobdate > 20240723",
         "SELECT * FROM table WHERE e.cobdate > 2024-07-23"),
        
        # Less than case
        ("SELECT * FROM table WHERE alias.cobdate < 20240823",
         "SELECT * FROM table WHERE alias.cobdate < 2024-08-23"),
        
        # Greater than or equal to case
        ("SELECT * FROM table WHERE cobdate >= 20240601",
         "SELECT * FROM table WHERE cobdate >= 2024-06-01"),
        
        # Less than or equal to case
        ("SELECT * FROM table WHERE t.cobdate <= 20241031",
         "SELECT * FROM table WHERE t.cobdate <= 2024-10-31"),
        
        # Multiple conditions
        ("SELECT * FROM table WHERE xyz.cobdate between 20240101 and 20241231 AND e.cobdate > 20240601",
         "SELECT * FROM table WHERE xyz.cobdate between 2024-01-01 and 2024-12-31 AND e.cobdate > 2024-06-01"),
        
        # Different aliases
        ("SELECT * FROM table WHERE t1.cobdate < 20240401 OR t2.cobdate >= 20240501",
         "SELECT * FROM table WHERE t1.cobdate < 2024-04-01 OR t2.cobdate >= 2024-05-01"),
        
        # Case with no dates to convert
        ("SELECT * FROM table WHERE id = 123",
         "SELECT * FROM table WHERE id = 123"),
        
        # Case with dates but no 'cobdate'
        ("SELECT * FROM table WHERE date between 20240101 and 20241231",
         "SELECT * FROM table WHERE date between 20240101 and 20241231"),
        
        # Complex case with subquery
        ("SELECT * FROM table1 WHERE exists (SELECT 1 FROM table2 WHERE table2.cobdate between 20240101 and 20241231) AND table1.cobdate > 20240601",
         "SELECT * FROM table1 WHERE exists (SELECT 1 FROM table2 WHERE table2.cobdate between 2024-01-01 and 2024-12-31) AND table1.cobdate > 2024-06-01"),
    ]

    for i, (input_sql, expected_output) in enumerate(test_cases, 1):
        result = convert_date_format_in_sql(input_sql)
        print(f"Test case {i}:")
        print(f"Input:    {input_sql}")
        print(f"Output:   {result}")
        print(f"Expected: {expected_output}")
        print("Pass" if result == expected_output else "Fail")
        print()

# Run the test cases
test_convert_date_format_in_sql()





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

# Test function
def test_convert_date_format_in_sql():
    test_cases = [
        # Mixed case keywords
        ("SELECT * FROM table WHERE xyz.cobdate BeTwEeN 20240101 and 20241231",
         "SELECT * FROM table WHERE xyz.cobdate BETWEEN 2024-01-01 AND 2024-12-31"),
        
        # Uppercase keywords
        ("SELECT * FROM table WHERE E.COBDATE > 20240723",
         "SELECT * FROM table WHERE E.COBDATE > 2024-07-23"),
        
        # Lowercase keywords
        ("select * from table where alias.cobdate < 20240823",
         "select * from table where alias.cobdate < 2024-08-23"),
        
        # Mixed case table alias
        ("SELECT * FROM table WHERE CoB.cobdate >= 20240601",
         "SELECT * FROM table WHERE CoB.cobdate >= 2024-06-01"),
        
        # Multiple conditions with mixed case
        ("SELECT * FROM table WHERE xyz.cobdate BETWEEN 20240101 AND 20241231 and e.cobdate > 20240601",
         "SELECT * FROM table WHERE xyz.cobdate BETWEEN 2024-01-01 AND 2024-12-31 and e.cobdate > 2024-06-01"),
        
        # Complex case with subquery and mixed case
        ("SELECT * FROM table1 WHERE EXISTS (SELECT 1 FROM table2 WHERE table2.cobdate BeTwEeN 20240101 and 20241231) AND table1.cobdate > 20240601",
         "SELECT * FROM table1 WHERE EXISTS (SELECT 1 FROM table2 WHERE table2.cobdate BETWEEN 2024-01-01 AND 2024-12-31) AND table1.cobdate > 2024-06-01"),
    ]

    for i, (input_sql, expected_output) in enumerate(test_cases, 1):
        result = convert_date_format_in_sql(input_sql)
        print(f"Test case {i}:")
        print(f"Input:    {input_sql}")
        print(f"Output:   {result}")
        print(f"Expected: {expected_output}")
        print("Pass" if result == expected_output else "Fail")
        print()

# Run the test cases
test_convert_date_format_in_sql()
