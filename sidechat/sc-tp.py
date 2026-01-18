#!/usr/bin/env python3
import json, sys, os, subprocess
from pathlib import Path
import platform

CONFIG=".config"
if platform.system() == "Darwin":
    CONFIG="Library/Application Support"

memfile=Path(f"~/{CONFIG}/sidechat").expanduser() / "memories.json"

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

elif "memory" in tool_name:
    fd = os.open(memfile, os.O_RDONLY | os.O_CREAT, mode=0o644)
    with os.fdopen(fd, 'r') as f:
        try:
            mems = json.load(f)
        except:
            mems = []

    if tool_name == "show_memory":
        print(mems)
    # this is save memory
    else:
        mems.append(args.get('memory'))
        with open(memfile, 'w') as f:
            json.dump(mems,f, indent=2)

else:
    print(json.dumps({"error": f"Unknown tool: {tool_name}"}))
    sys.exit(1)
