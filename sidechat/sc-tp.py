#!/usr/bin/env python3
import json, sys, os, subprocess
from pathlib import Path

input_data = json.loads(sys.stdin.read())
tool_name = input_data['name']
args = input_data.get('arguments', {})

if tool_name == "list_files":
    DIR = Path(args.get('path') or '.').expanduser()
    mp3s = [f.name for f in DIR.glob("*")]
    print(json.dumps(mp3s))

elif tool_name == "read_file":
    with open(Path(args.get('path')).expanduser() / args.get('filename'), 'r') as r:
        print(r.read())

else:
    print(json.dumps({"error": f"Unknown tool: {tool_name}"}))
    sys.exit(1)
