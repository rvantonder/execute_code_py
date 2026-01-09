# Code-Only Environment - Capabilities Reference

## What Claude CAN Do

### ✅ Mathematical Computation

**Simple arithmetic**:
```python
result = (15 * 20) + (30 / 2)
# Returns: 315.0
```

**Advanced math**:
```python
import math
result = math.sqrt(73.5)  # Square root
result = math.sin(math.pi / 2)  # Trigonometry
result = math.factorial(10)  # Factorial
```

**Complex numbers**:
```python
result = complex(3, 4) * complex(2, 1)
# Returns: (2+11j)
```

### ✅ Data Processing

**Lists and comprehensions**:
```python
data = [1, 2, 3, 4, 5]
result = [x**2 for x in data if x % 2 == 0]
# Returns: [4, 16]
```

**Dictionaries**:
```python
data = {"a": 1, "b": 2, "c": 3}
result = {k: v*2 for k, v in data.items()}
# Returns: {"a": 2, "b": 4, "c": 6}
```

**Data transformation**:
```python
raw = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
result = {name: age for name, age in raw}
# Returns: {"Alice": 25, "Bob": 30, "Charlie": 35}
```

### ✅ String Processing

**Manipulation**:
```python
text = "hello world"
result = text.upper().replace(" ", "_")
# Returns: "HELLO_WORLD"
```

**Parsing**:
```python
csv_line = "Alice,25,Engineer"
result = csv_line.split(",")
# Returns: ["Alice", "25", "Engineer"]
```

**Formatting**:
```python
name, age = "Alice", 25
result = f"{name} is {age} years old"
# Returns: "Alice is 25 years old"
```

### ✅ JSON Processing

**Parsing**:
```python
import json
json_string = '{"name": "Alice", "age": 25}'
result = json.loads(json_string)
# Returns: {"name": "Alice", "age": 25}
```

**Formatting**:
```python
import json
data = {"name": "Alice", "age": 25}
result = json.dumps(data, indent=2)
# Returns: formatted JSON string
```

### ✅ Data Structures

**Sets**:
```python
a = {1, 2, 3}
b = {2, 3, 4}
result = a & b  # Intersection
# Returns: {2, 3}
```

**Tuples**:
```python
data = [(1, "a"), (2, "b"), (3, "c")]
result = dict(data)
# Returns: {1: "a", 2: "b", 3: "c"}
```

**Named tuples**:
```python
from collections import namedtuple
Person = namedtuple("Person", ["name", "age"])
result = Person("Alice", 25)
# Returns: Person(name='Alice', age=25)
```

### ✅ Algorithms

**Sorting**:
```python
data = [3, 1, 4, 1, 5, 9, 2, 6]
result = sorted(data)
# Returns: [1, 1, 2, 3, 4, 5, 6, 9]
```

**Filtering**:
```python
data = range(20)
result = list(filter(lambda x: x % 3 == 0, data))
# Returns: [0, 3, 6, 9, 12, 15, 18]
```

**Mapping**:
```python
data = [1, 2, 3, 4, 5]
result = list(map(lambda x: x**2, data))
# Returns: [1, 4, 9, 16, 25]
```

### ✅ Statistical Operations

**Basic statistics**:
```python
data = [1, 2, 3, 4, 5]
result = {
    "sum": sum(data),
    "mean": sum(data) / len(data),
    "min": min(data),
    "max": max(data)
}
```

**Using statistics module**:
```python
import statistics
data = [1, 2, 3, 4, 5]
result = {
    "mean": statistics.mean(data),
    "median": statistics.median(data),
    "stdev": statistics.stdev(data)
}
```

### ✅ Date/Time Operations

**Current time**:
```python
from datetime import datetime
result = datetime.now().isoformat()
# Returns: "2026-01-09T14:30:00.123456"
```

**Date arithmetic**:
```python
from datetime import datetime, timedelta
now = datetime.now()
future = now + timedelta(days=30)
result = future.strftime("%Y-%m-%d")
# Returns: "2026-02-08"
```

**Parsing**:
```python
from datetime import datetime
date_str = "2026-01-09"
result = datetime.strptime(date_str, "%Y-%m-%d")
```

### ✅ Regular Expressions

**Pattern matching**:
```python
import re
text = "Email: alice@example.com"
result = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
# Returns: ["alice@example.com"]
```

**Substitution**:
```python
import re
text = "Phone: 123-456-7890"
result = re.sub(r'(\d{3})-(\d{3})-(\d{4})', r'(\1) \2-\3', text)
# Returns: "Phone: (123) 456-7890"
```

### ✅ Encoding/Decoding

**Base64**:
```python
import base64
data = "Hello World"
encoded = base64.b64encode(data.encode()).decode()
result = encoded
# Returns: "SGVsbG8gV29ybGQ="
```

**URL encoding**:
```python
from urllib.parse import quote
result = quote("Hello World!")
# Returns: "Hello%20World%21"
```

### ✅ Hashing

**MD5/SHA256**:
```python
import hashlib
data = "Hello World"
result = hashlib.sha256(data.encode()).hexdigest()
# Returns: hash string
```

### ✅ Code Generation

**Generate Python code**:
```python
def generate_class(name, fields):
    code = f"class {name}:\n"
    code += "    def __init__(self"
    for field in fields:
        code += f", {field}"
    code += "):\n"
    for field in fields:
        code += f"        self.{field} = {field}\n"
    return code

result = generate_class("Person", ["name", "age"])
# Returns: Python class code as string
```

### ✅ Logic and Control Flow

**Conditionals**:
```python
def categorize(age):
    if age < 13:
        return "child"
    elif age < 20:
        return "teenager"
    else:
        return "adult"

result = [categorize(age) for age in [5, 15, 25]]
# Returns: ["child", "teenager", "adult"]
```

**Loops**:
```python
result = []
for i in range(5):
    for j in range(i):
        result.append((i, j))
# Returns: [(1,0), (2,0), (2,1), ...]
```

## What Claude CANNOT Do

### ❌ File System Operations

**Cannot read files**:
```python
# This won't work - you'd have to provide the code to user
with open('config.json') as f:
    data = f.read()
```

**Cannot write files**:
```python
# This won't work - you'd have to provide the code to user
with open('output.txt', 'w') as f:
    f.write('data')
```

**Cannot check file existence**:
```python
# This won't work
import os
exists = os.path.exists('file.txt')
```

**Workaround**: Provide the code to the user, they can run it themselves

### ❌ System Commands

**Cannot run bash**:
```python
# This won't work
import subprocess
subprocess.run(['ls', '-la'])
```

**Cannot execute system commands**:
```python
# This won't work
import os
os.system('git status')
```

**Workaround**: Tell user what command to run, or provide script

### ❌ Network Operations

**Cannot fetch URLs**:
```python
# This won't work (no urllib/requests in execute_code)
import urllib.request
urllib.request.urlopen('https://example.com')
```

**Cannot make API calls**:
```python
# This won't work
import requests
requests.get('https://api.example.com')
```

**Workaround**: Ask user to provide data, or generate code they can run

### ❌ Search/Discovery Operations

**Cannot search for files**:
- No Glob tool access
- Cannot find files by pattern

**Cannot search file contents**:
- No Grep tool access
- Cannot search across codebase

**Cannot read directory structure**:
- No browsing capabilities
- Cannot discover what files exist

**Workaround**: Ask user to provide file list or directory structure

### ❌ Code Editing

**Cannot edit existing files**:
- No Edit tool access
- Cannot modify files in place

**Cannot create new files**:
- No Write tool access
- Cannot save generated code

**Workaround**: Generate code as string in result, user saves it

### ❌ Multi-Agent Operations

**Cannot spawn sub-agents**:
- No Task tool access
- Cannot delegate to specialized agents

**Cannot parallelize**:
- No concurrent agent execution
- Single execution context only

**Workaround**: Handle everything in single execution, or break into steps

## Capability Matrix

| Operation | Available | Via | Notes |
|-----------|-----------|-----|-------|
| Math | ✅ | execute_code | Full Python math library |
| Data processing | ✅ | execute_code | Lists, dicts, sets, etc. |
| String manipulation | ✅ | execute_code | Full string methods |
| JSON | ✅ | execute_code | json module |
| Regex | ✅ | execute_code | re module |
| Date/time | ✅ | execute_code | datetime module |
| Hashing | ✅ | execute_code | hashlib module |
| Encoding | ✅ | execute_code | base64, urllib |
| Logic | ✅ | execute_code | Conditionals, loops |
| Code generation | ✅ | execute_code | As string output |
| Read files | ❌ | - | Blocked by hooks |
| Write files | ❌ | - | Blocked by hooks |
| Run commands | ❌ | - | Blocked by hooks |
| Network requests | ❌ | - | No packages available |
| Search files | ❌ | - | Blocked by hooks |
| Edit code | ❌ | - | Blocked by hooks |
| Spawn agents | ❌ | - | Blocked by hooks |

## Standard Library Available

The Python standard library is fully available (packages in `.venv/`):

- `math` - Mathematical functions
- `statistics` - Statistical functions
- `json` - JSON encoding/decoding
- `re` - Regular expressions
- `datetime` - Date and time
- `collections` - Data structures
- `itertools` - Iterator tools
- `functools` - Functional programming
- `hashlib` - Hashing algorithms
- `base64` - Base64 encoding
- `urllib.parse` - URL parsing (not fetching)
- `random` - Random numbers
- `string` - String operations
- `decimal` - Decimal arithmetic
- `fractions` - Rational numbers
- `typing` - Type hints
- And many more...

## Third-Party Packages

**Default**: Only `mcp` package installed

**To add more**:
```bash
source .venv/bin/activate
pip install numpy pandas matplotlib
```

Then available in execute_code:
```python
import numpy as np
result = np.array([1, 2, 3]).mean()
```

## Summary

**Strong capabilities**:
- Pure computation (math, logic, algorithms)
- Data transformation and processing
- Code generation as output
- Standard library operations

**No capabilities**:
- File system I/O
- System commands
- Network operations
- Multi-tool workflows

**Mental model**: Think of Claude as a Python REPL with excellent language understanding but no I/O beyond stdin/stdout.
