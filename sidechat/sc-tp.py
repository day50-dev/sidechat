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


elif tool_name == "create_file":
    file_path = Path(args.get('path') or '.').expanduser() / args.get('filename')

elif tool_name == "edit_file":
    file_path = Path(args.get('path') or '.').expanduser() / args.get('filename')
    line_start = args.get('line_start')
    line_end = args.get('line_end')
    old_content = args.get('old_content')
    new_content = args.get('new_content')
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Validate line range and fetch content
        if line_start < 1 or line_end > len(lines) or line_start > line_end:
            rpc({
                "ok": False,
                "reason": f"Invalid line range: line_start={line_start}, line_end={line_end}, total_lines={len(lines)}"
            })
            sys.exit(0)
        
        # Get the actual content being edited
        lines_in_range = ''.join(lines[line_start - 1:line_end])
        
        # Verify content matches (sanity check)
        if lines_in_range != old_content:
            rpc({
                "ok": False,
                "reason": "Content mismatch. Reread the file",
                "line_start": line_start,
                "line_end": line_end,
                "expected": old_content[:100],  # partial view for debugging
                "actual": lines_in_range[:100]
            })
            sys.exit(0)
        
        # Perform the edit
        lines[line_start - 1:line_end] = [new_content + '\n'] if line_start == line_end else [new_content + '\n'] + lines[line_end:]
        
        with open(file_path, 'w') as f:
            f.writelines(lines)
        
        rpc({
            "ok": True,
            "path": str(file_path),
            "line_start": line_start,
            "line_end": line_end,
            "old_length": line_end - line_start + 1,
            "new_length": 1 if line_start == line_end else len(lines[line_end:]) + 1
        })

    except Exception as e:
        rpc({
            "ok": False,
            "error": str(e),
            "path": str(file_path)
        })

elif tool_name == "read_file":
    file_path = Path(args.get('path') or '.').expanduser() / args.get('filename')
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        formatted_lines = []
        for i, line in enumerate(lines, 1):
            formatted_lines.append(f"<line number={i}>{line}</line>")
        
        rpc("".join(formatted_lines))
    except Exception as e:
        rpc({
            "ok": False,
            "error": str(e),
            "path": str(file_path)
        })

elif tool_name == "read_pydoc":
    rpc(subprocess.run(
        ["pydoc", args['object']],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False      
    ).stdout)

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

