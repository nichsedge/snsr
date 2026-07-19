---
description: Publish package to PyPI using uv
---

1. Bump the patch version
// turbo
uv version --bump patch

2. Clean dist directory
// turbo
rm -rf dist

3. Build the distribution
// turbo
uv build

4. Publish the package
// turbo
uv publish
