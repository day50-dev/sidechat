#!/usr/bin/env python3
import json, sys, os, subprocess
from pathlib import Path
import platform

CONFIG=".config"
if platform.system() == "Darwin":
    CONFIG="Library/Application Support"

memfile=Path(f"~/{CONFIG}/sidechat").expanduser() / "memories.json"

def rpc(data):
    print(json.dumps({"jsonrpc": "2.0", "result": data}), flush=True)

for res in sys.stdin: 
    input_data = json.loads(res)
    if input_data['method'] == 'initialize':
        rpc({
            "protocolVersion":"2024-11-05",
            "capabilities": {
                "tools":{"listChanged":True},"resources":{"listChanged":True},"completions":{}
            },
            "serverInfo":{"name":"demo", "version":"1.0.0"}
        })

    if input_data['method'] == 'tools/call':
        params = input_data.get('params')
        tool_name = params['name']
        args = params.get('arguments', {})
        break


if tool_name == "list_files":
    DIR = Path(args.get('path') or '.').expanduser()
    rpc([f.name for f in DIR.glob("*")])

elif tool_name == "read_file":
    with open(Path(args.get('path')).expanduser() / args.get('filename'), 'r') as r:
        rpc(r.read())

elif tool_name == "read_man_section":
    rpc(subprocess.run(
        ["mansnip", "--llm", args['manpage'], args['section']],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False      
    ).stdout)

elif "memory" in tool_name:
    fd = os.open(memfile, os.O_RDONLY | os.O_CREAT, mode=0o644)
    with os.fdopen(fd, 'r') as f:
        try:
            mems = json.load(f)
        except:
            mems = []

    if tool_name == "show_memory":
        rpc(mems)

    # this is save memory
    else:
        mems.append(args.get('memory'))
        with open(memfile, 'w') as f:
            json.dump(mems,f, indent=2)

        rpc({"ok": True})

