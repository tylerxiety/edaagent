"""
Common utilities.
"""

from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Image, display
import json
import pprint
import textwrap


def print_generated_code(output, show_tags=False):
    """
    Pretty-print output from generate_eda_code or execute_code.
    
    Args:
        output: Either:
            - String from generate_eda_code (code with/without tags)
            - Dict from execute_code (execution results)
        show_tags: Whether to show XML tags (only for string input)
    """  
    # Handle dict output (from execute_code)
    if isinstance(output, dict):
        print("=" * 70)
        print("full output")
        print("=" * 70)
        
        # Print code
        if "code" in output:
            print("\n📝 CODE:")
            print("-" * 70)
            print(output["code"])
        
        # Print stdout
        if output.get("stdout"):
            print("\n📤 OUTPUT:")
            print("-" * 70)
            print(output["stdout"])
        
        # Print result
        if output.get("result") is not None:
            print("\n✅ RESULT:")
            print("-" * 70)
            if isinstance(output["result"], (dict, list)):
                pprint.pprint(output["result"], width=100, sort_dicts=False)
            else:
                print(output["result"])
        
        # Print error
        if output.get("error"):
            print("\n❌ ERROR:")
            print("-" * 70)
            print(output["error"])
        
        # Print image path
        if output.get("image_path"):
            print(f"\n📈 VISUALIZATION: {output['image_path']}")
            display(Image(filename=output["image_path"]))
        
        return
    
    # Handle string output (from generate_eda_code)
    if isinstance(output, str):
        # Extract code from tags if present
        match = re.search(r"<execute_python>(.*?)</execute_python>", output, re.DOTALL | re.IGNORECASE)
        
        if match:
            code = match.group(1).strip()
            
            if show_tags:
                print("=" * 70)
                print("FULL OUTPUT (with tags)")
                print("=" * 70)
                print(output)
                print("\n")
            
            print("=" * 70)
            print("GENERATED CODE")
            print("=" * 70)
            print(code)
        else:
            # No tags found, wrap text for readability
            print("=" * 70)
            print("OUTPUT")
            print("=" * 70)
            # Wrap text at 80 characters for better readability
            wrapped_output = textwrap.fill(output, width=80)
            print(wrapped_output)



def print_response(
    response,
    show_reasoning=True,
    show_usage=True,
    show_metadata=True,
    show_config=False
):
    """
    Pretty-print ALL content from OpenAI Response object.
    
    Args:
        response: Response object from OpenAI API (responses.create)
        show_reasoning: Whether to show reasoning details
        show_usage: Whether to show token usage stats
        show_metadata: Whether to show metadata (model, id, status, etc.)
        show_config: Whether to show configuration (temperature, etc.)
        
    Returns:
        Extracted text content as string
    """
    print("=" * 70)
    print("OPENAI RESPONSE")
    print("=" * 70)
    
    # Show metadata
    if show_metadata:
        print(f"\n📋 METADATA:")
        print(f"  Model:      {response.model}")
        print(f"  ID:         {response.id}")
        print(f"  Status:     {response.status}")
        print(f"  Created:    {response.created_at}")
        print(f"  Object:     {response.object}")
        if response.service_tier:
            print(f"  Service:    {response.service_tier}")
    
    # Show configuration
    if show_config:
        print(f"\n⚙️  CONFIGURATION:")
        print(f"  Temperature:  {response.temperature}")
        print(f"  Top P:        {response.top_p}")
        if hasattr(response, 'reasoning') and response.reasoning:
            print(f"  Reasoning:    effort={response.reasoning.effort}")
        if hasattr(response, 'text') and response.text:
            print(f"  Verbosity:    {response.text.verbosity}")
    
    # Show instructions if present
    if response.instructions:
        print(f"\n📝 INSTRUCTIONS:")
        print("-" * 70)
        print(response.instructions)
    
    # Extract and display all output content
    text_content = []
    
    print(f"\n📤 OUTPUT:")
    print("-" * 70)
    
    for i, item in enumerate(response.output):
        item_type = getattr(item, 'type', 'unknown')
        
        # Handle reasoning items
        if item_type == 'reasoning':
            if show_reasoning:
                print(f"\n  [{i}] REASONING ITEM:")
                print(f"      ID: {getattr(item, 'id', 'N/A')}")
                if hasattr(item, 'summary') and item.summary:
                    print(f"      Summary: {item.summary}")
                else:
                    print(f"      Summary: (not available)")
                if hasattr(item, 'status') and item.status:
                    print(f"      Status: {item.status}")
        
        # Handle message items
        elif item_type == 'message':
            print(f"\n  [{i}] MESSAGE:")
            print(f"      ID:     {getattr(item, 'id', 'N/A')}")
            print(f"      Role:   {getattr(item, 'role', 'N/A')}")
            print(f"      Status: {getattr(item, 'status', 'N/A')}")
            
            # Extract content from message
            if hasattr(item, 'content'):
                for j, content_item in enumerate(item.content):
                    content_type = getattr(content_item, 'type', 'unknown')
                    
                    if content_type == 'output_text':
                        text = getattr(content_item, 'text', '')
                        text_content.append(text)
                        print(f"\n      Content [{j}] - TEXT:")
                        print(f"      {'-' * 60}")
                        # Indent the text content
                        for line in text.split('\n'):
                            print(f"      {line}")
                    else:
                        print(f"\n      Content [{j}] - {content_type.upper()}")
    
    # Show main text content summary
    if text_content:
        full_text = "\n\n".join(text_content)
    else:
        print("\n⚠️  No text content found in response")
        full_text = ""
    
    # Show token usage
    if show_usage and hasattr(response, 'usage') and response.usage:
        print(f"\n📊 TOKEN USAGE:")
        print("-" * 70)
        usage = response.usage
        
        # Input tokens
        print(f"  Input tokens:   {usage.input_tokens:,}")
        if hasattr(usage, 'input_tokens_details') and usage.input_tokens_details:
            cached = getattr(usage.input_tokens_details, 'cached_tokens', 0)
            if cached:
                print(f"    └─ cached:    {cached:,}")
        
        # Output tokens
        print(f"  Output tokens:  {usage.output_tokens:,}")
        if hasattr(usage, 'output_tokens_details') and usage.output_tokens_details:
            reasoning = getattr(usage.output_tokens_details, 'reasoning_tokens', 0)
            if reasoning:
                print(f"    └─ reasoning: {reasoning:,}")
        
        # Total
        print(f"  Total tokens:   {usage.total_tokens:,}")
    
    # Show error if present
    if response.error:
        print(f"\n❌ ERROR:")
        print("-" * 70)
        print(response.error)
    
    print("=" * 70)
    
    return full_text




def load_data(file_path):
    """
    Load data from CSV or Excel file.
    
    Args:
        file_path: Path to the data file
        
    Returns:
        pandas DataFrame
        
    Raises:
        ValueError: If file format is not supported or file doesn't exist
    """
    path = Path(file_path)
    
    if not path.exists():
        raise ValueError(f"File not found: {file_path}")
    
    # Determine loader based on file extension
    if path.suffix.lower() == '.csv':
        df = pd.read_csv(file_path)
    elif path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}. Use .csv, .xlsx, or .xls")
    
    # Basic validation
    if df.empty:
        raise ValueError("Loaded DataFrame is empty")
    
    print(f"✓ Loaded data: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def get_schema(df):
    """
    generate schema and metadata from a df
    """
    schema_info = []
    schema_info.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    schema_info.append(f"\nColumns:")
    for col in df.columns:
        dtype = df[col].dtype
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        schema_info.append(f"  - {col}: {dtype} (nulls: {null_count}, {null_pct:.1f}%)")
    
    schema_info.append(f"\nFirst 3 rows:")
    schema_info.append(df.head(3).to_string())
    
    schema_text = "\n".join(schema_info)

    return schema_text


def print_wrapped(text, width=80):
    """
    Print text with proper wrapping, preserving bullet points.
    
    Args:
        text: Text to print
    """
    for line in text.split('\n'):
        if line.strip().startswith(('-', '*', '•')) or (line.strip() and line.strip()[0].isdigit()):
            # Preserve bullet formatting
            print(textwrap.fill(line, width=width, 
                            subsequent_indent='  ',
                            break_long_words=False))
        else:
            print(textwrap.fill(line, width=width))