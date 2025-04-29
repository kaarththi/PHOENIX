# Phoenix Programming Language - Single File Interpreter
# File: ma.py

import re

print("🐦‍🔥 Phoenix Programming Language 🔥")
print("Type 'exit' to quit.\n")

variables = {}
functions = {}

def eval_expression(expr):
    expr = expr.strip()
    try:
        return eval(expr, {}, variables)
    except:
        # Attempt to resolve plus expressions
        parts = expr.split(" plus ")
        result = ""
        for part in parts:
            part = part.strip()
            if part.startswith('"') and part.endswith('"'):
                result += part.strip('"')
            elif part in variables:
                result += str(variables[part])
            else:
                result += part
        return result

def run_function(name):
    if name in functions:
        for line in functions[name]:
            run_line(line)
    else:
        print("❌ Unknown function:", name)

def run_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return

    if line.startswith("gescieppan"):
        # Variable creation
        match = re.match(r'gescieppan (\w+) be (.+)', line)
        if match:
            var, val = match.groups()
            if val.startswith('"') and val.endswith('"'):
                variables[var] = val.strip('"')
            elif val in variables:
                variables[var] = variables[val]
            else:
                try:
                    variables[var] = eval(val, {}, variables)
                except:
                    variables[var] = val
    elif line.startswith("scry "):
        expr = line[5:]
        try:
            print(eval_expression(expr))
        except Exception as e:
            print("❌ Error:", e)
    elif line.startswith("asketh "):
        parts = line.split(" be ")
        if len(parts) == 2:
            varname = parts[0].replace("asketh", "").strip()
            prompt = parts[1].strip().strip('"')
            val = input(prompt + " ")
            variables[varname] = val
    elif line.startswith("spell "):
        match = re.match(r'spell (\w+) be:', line)
        if match:
            name = match.group(1)
            body = []
            while True:
                try:
                    subline = input(".. ").strip()
                    if not subline:
                        break
                    body.append(subline)
                except KeyboardInterrupt:
                    print("\n❌ Interrupted")
                    return
            functions[name] = body
            print(f"(function '{name}' defined)")
    elif line.startswith("summon "):
        funcname = line.replace("summon", "").strip()
        run_function(funcname)
    elif line.startswith("repeat "):
        match = re.match(r'repeat (\d+) times:', line)
        if match:
            count = int(match.group(1))
            body = []
            while True:
                subline = input(".. ").strip()
                if not subline:
                    break
                body.append(subline)
            for _ in range(count):
                for b in body:
                    run_line(b)
    elif line == "exit":
        print("👋 Exiting Phoenix.")
        exit()
    else:
        print("❌ Unknown command.")

def main():
    try:
        while True:
            line = input("🔥>> ")
            run_line(line)
    except KeyboardInterrupt:
        print("\n👋 Exiting Phoenix.")

if __name__ == "__main__":
    main()
