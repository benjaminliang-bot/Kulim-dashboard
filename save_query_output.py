"""
Helper script to save query output to file
This makes it easy to save the query output for auto_export_merchants.py

Usage:
1. Copy the query output from the MCP tool result
2. Paste it when prompted
3. It will be saved to query_output.txt
4. Then run: python auto_export_merchants.py
"""

def save_query_output():
    """
    Prompt user to paste query output and save to file
    """
    print("=" * 70)
    print("Save Query Output Helper")
    print("=" * 70)
    print()
    print("Instructions:")
    print("1. Copy the FULL query output from the MCP tool result")
    print("2. Paste it below (it should start with '| merchant_id_nk | ...')")
    print("3. Press Enter twice when done")
    print()
    print("-" * 70)
    print("Paste query output here:")
    print("-" * 70)
    
    lines = []
    empty_line_count = 0
    
    try:
        while True:
            line = input()
            if line.strip():
                lines.append(line)
                empty_line_count = 0
            else:
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
                lines.append(line)
    except EOFError:
        pass
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        return
    
    query_output = '\n'.join(lines)
    
    if not query_output.strip():
        print("\n❌ No output provided. Exiting.")
        return
    
    # Save to file
    try:
        with open('query_output.txt', 'w', encoding='utf-8') as f:
            f.write(query_output)
        
        print()
        print("=" * 70)
        print("✅ Query output saved to query_output.txt")
        print("=" * 70)
        print()
        print("Now you can run: python auto_export_merchants.py")
        print("The script will automatically process the saved query output!")
        
    except Exception as e:
        print(f"\n❌ Error saving file: {e}")


if __name__ == "__main__":
    save_query_output()

