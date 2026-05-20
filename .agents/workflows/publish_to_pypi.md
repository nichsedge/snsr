---
description: Publish package to PyPI using uv
---

1. Bump the patch version
// turbo
python3 -c 'import re; txt = open("pyproject.toml").read(); new_txt = re.sub(r"version = \"(\d+)\.(\d+)\.(\d+)\"", lambda m: f"version = \"{m.group(1)}.{m.group(2)}.{int(m.group(3))+1}\"", txt); open("pyproject.toml", "w").write(new_txt); print(f"Bumped version to {re.search(r"version = \"(.*?)\"", new_txt).group(1)}")'

2. Clean dist directory
// turbo
rm -rf dist

3. Build the distribution
// turbo
uv build

4. Publish the package
// turbo
uv publish
