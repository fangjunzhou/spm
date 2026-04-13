# Usage

## Quick start

1. Implement a `SlangPackage` subclass.
2. Register the package with `SlangPackageManager.register_package`.
3. Instantiate `SlangPackageManager` to build the dependency graph.

```python
from spm_slang.package import SlangPackage
from spm_slang.package_manager import SlangPackageManager


class MyPackage(SlangPackage):
    @staticmethod
    def name() -> str:
        return "my-package"

    @staticmethod
    def shader_paths() -> list[str]:
        return ["shaders/my_package.slang"]

    def build(self):
        return self._device.load_module_from_source("my-package", "// shader code")


SlangPackageManager.register_package(MyPackage)
manager = SlangPackageManager()
module_map = manager.module_map
```

## Dependency ordering

Dependencies are declared by overriding `dependencies()` on a package class. The
package manager builds packages in topological order and raises `ValueError` on
missing registrations or cycles.
