"""
AI Tools Usage Check - Query Grabber AI tooling usage statistics
Checks AI Tools usage and adoption statistics by querying ai_tooling_usage.grabbers_ai_usage_summary
"""

import re
from datetime import datetime
from typing import Optional, Dict, List, Any

def validate_email(email: str) -> bool:
    """Validate Grab email format: firstname.lastname@grabtaxi.com"""
    pattern = r'^[a-z]+\.[a-z]+@grabtaxi\.com$'
    return bool(re.match(pattern, email.lower()))

def format_email(email: str) -> str:
    """Format email to lowercase for consistency"""
    return email.lower().strip()

def generate_usage_query(email: str, limit: int = 100) -> str:
    """Generate SQL query for AI tooling usage"""
    formatted_email = format_email(email)
    
    query = f"""
SELECT *
FROM ai_tooling_usage.grabbers_ai_usage_summary
WHERE email_work = '{formatted_email}'
ORDER BY date DESC
LIMIT {limit}
"""
    return query.strip()

def format_usage_table(data: List[Dict]) -> str:
    """Format usage data as ASCII table"""
    if not data:
        return "No data available"
    
    # Extract column names
    columns = list(data[0].keys())
    
    # Calculate column widths
    col_widths = {}
    for col in columns:
        col_widths[col] = max(
            len(str(col)),
            max((len(str(row.get(col, ''))) for row in data), default=0)
        )
        # Cap width at 30 for readability
        col_widths[col] = min(col_widths[col], 30)
    
    # Build table
    lines = []
    
    # Header
    header = " | ".join(str(col).ljust(col_widths[col]) for col in columns)
    lines.append(header)
    lines.append("-" * len(header))
    
    # Rows
    for row in data:
        row_str = " | ".join(
            str(row.get(col, '')).ljust(col_widths[col])[:col_widths[col]]
            for col in columns
        )
        lines.append(row_str)
    
    return "\n".join(lines)

def calculate_adoption_metrics(data: List[Dict]) -> Dict[str, Any]:
    """Calculate adoption metrics from usage data"""
    if not data:
        return {}
    
    metrics = {
        'total_records': len(data),
        'date_range': {},
        'tools_used': set(),
        'usage_frequency': {},
        'recent_activity': {}
    }
    
    # Extract dates
    dates = []
    for row in data:
        date_val = row.get('date')
        if date_val:
            dates.append(date_val)
    
    if dates:
        metrics['date_range'] = {
            'earliest': min(dates),
            'latest': max(dates)
        }
    
    # Extract tools (assuming there's a tool column)
    tool_columns = [col for col in data[0].keys() if 'tool' in col.lower() or 'usage' in col.lower()]
    for row in data:
        for col in tool_columns:
            if row.get(col):
                metrics['tools_used'].add(str(row.get(col)))
    
    metrics['tools_used'] = list(metrics['tools_used'])
    metrics['unique_tools'] = len(metrics['tools_used'])
    
    return metrics

def generate_dashboard(data: List[Dict], email: str) -> str:
    """Generate a graphical dashboard of usage statistics"""
    if not data:
        return "No data available for dashboard"
    
    metrics = calculate_adoption_metrics(data)
    
    dashboard = []
    dashboard.append("=" * 80)
    dashboard.append("AI TOOLS USAGE DASHBOARD")
    dashboard.append("=" * 80)
    dashboard.append(f"Email: {email}")
    dashboard.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    dashboard.append("")
    
    # Summary Stats
    dashboard.append("📊 SUMMARY STATISTICS")
    dashboard.append("-" * 80)
    dashboard.append(f"Total Records: {metrics.get('total_records', 0)}")
    dashboard.append(f"Unique Tools: {metrics.get('unique_tools', 0)}")
    
    if metrics.get('date_range'):
        dashboard.append(f"Date Range: {metrics['date_range']['earliest']} to {metrics['date_range']['latest']}")
    
    dashboard.append("")
    
    # Tools Used
    if metrics.get('tools_used'):
        dashboard.append("🛠️  TOOLS USED")
        dashboard.append("-" * 80)
        for tool in sorted(metrics['tools_used']):
            dashboard.append(f"  • {tool}")
        dashboard.append("")
    
    # Recent Activity (last 5 records)
    if len(data) > 0:
        dashboard.append("📅 RECENT ACTIVITY (Last 5 Records)")
        dashboard.append("-" * 80)
        for i, row in enumerate(data[:5], 1):
            dashboard.append(f"\nRecord {i}:")
            for key, value in row.items():
                if value is not None:
                    dashboard.append(f"  {key}: {value}")
        dashboard.append("")
    
    dashboard.append("=" * 80)
    
    return "\n".join(dashboard)

def check_ai_tools_usage(email: Optional[str] = None) -> Dict[str, Any]:
    """
    Main function to check AI tools usage
    
    Args:
        email: Grab email address (firstname.lastname@grabtaxi.com)
    
    Returns:
        Dictionary with query results and formatted output
    """
    result = {
        'success': False,
        'error': None,
        'data': None,
        'query': None,
        'formatted_table': None,
        'dashboard': None,
        'metrics': None
    }
    
    # Step 1: Check MCP availability
    # Note: In Cursor chat, MCP tools are available via function calls
    # We'll proceed assuming MCP is available (will be called by AI)
    
    # Step 2: Request/Validate email
    if not email:
        result['error'] = "Email required. Format: firstname.lastname@grabtaxi.com"
        return result
    
    if not validate_email(email):
        result['error'] = f"Invalid email format: {email}\nRequired format: firstname.lastname@grabtaxi.com"
        return result
    
    # Step 3: Generate query
    query = generate_usage_query(email)
    result['query'] = query
    
    print("=" * 80)
    print("AI TOOLS USAGE CHECK")
    print("=" * 80)
    print(f"Email: {email}")
    print(f"\nGenerated Query:")
    print("-" * 80)
    print(query)
    print("-" * 80)
    print("\n⚠️  Execute this query using MCP tool:")
    print("   mcp_mcp-grab-data_run_presto_query")
    print("\nOr if mcp-grab-data is not available, try:")
    print("   mcp_mcp-hubble_run_presto_query")
    print("=" * 80)
    
    return result

if __name__ == '__main__':
    # Example usage
    email = input("Enter Grab email (firstname.lastname@grabtaxi.com): ").strip()
    result = check_ai_tools_usage(email)
    
    if result['error']:
        print(f"\n❌ Error: {result['error']}")
    else:
        print(f"\n✅ Query generated successfully")
        print(f"   Execute via MCP to get results")

