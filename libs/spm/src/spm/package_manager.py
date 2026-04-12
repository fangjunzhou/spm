from typing import Dict, List, Optional, Sequence, TypedDict, Union
import logging
from collections import deque
import slangpy as spy
from slangpy.core.utils import BindlessDesc, NativeHandle, PathLike

from spm.package import SlangPackage

logger = logging.getLogger(__name__)

# A registry to keep track of all registered Slang packages.
packages: Dict[str, type[SlangPackage]] = {}


class DeviceConfiguration(TypedDict, total=False):
    type: spy.DeviceType
    enable_debug_layers: bool
    adapter_luid: Optional[Sequence[int]]
    include_paths: Sequence[Union[str, PathLike[str]]]
    enable_cuda_interop: bool
    enable_print: bool
    enable_hot_reload: bool
    enable_compilation_reports: bool
    existing_device_handles: Optional[Sequence[NativeHandle]]
    bindless_options: Optional[BindlessDesc]


DEFAULT_DEVICE_CONFIGURATION: DeviceConfiguration = {
    "type": spy.DeviceType.automatic,
    "enable_debug_layers": False,
    "adapter_luid": None,
    "include_paths": [],
    "enable_cuda_interop": False,
    "enable_print": False,
    "enable_hot_reload": True,
    "enable_compilation_reports": False,
    "existing_device_handles": None,
    "bindless_options": None,
}


class SlangPackageManager:
    def __init__(self, device_config: Optional[DeviceConfiguration] = None) -> None:
        merged_device_config: DeviceConfiguration = {
            **DEFAULT_DEVICE_CONFIGURATION,
            **(device_config or {}),
        }

        include_paths = [
            *merged_device_config.get("include_paths", ()),
            *self._get_shader_paths(),
        ]
        merged_device_config["include_paths"] = include_paths

        logger.debug(
            f"Initializing SlangPackageManager with include paths: {include_paths}"
        )
        sorted_packages = self._sort_packages_by_dependencies()
        logger.debug(
            f"Sorted packages based on dependencies: {[pkg.name() for pkg in sorted_packages]}"
        )
        # Create a Slang module map.
        self._module_map: Dict[str, spy.Module] = {}
        # Create a Slang device with the collected include paths.
        self._device = spy.create_device(**merged_device_config)
        # Build each package in the sorted order and store the resulting modules in the module map.
        for package_cls in sorted_packages:
            logger.debug(f"Building package '{package_cls.name()}'")
            dependency_modules = []
            for dep_cls in package_cls.dependencies():
                dep_name = dep_cls.name()
                if dep_name not in self._module_map:
                    raise ValueError(
                        f"Dependency '{dep_name}' for package '{package_cls.name()}' has not been built yet."
                    )
                dependency_modules.append(self._module_map[dep_name])
            module = package_cls(self._device, dependency_modules)._module
            self._module_map[package_cls.name()] = module
            logger.debug(
                f"Built package '{package_cls.name()}' and stored module in module map"
            )

    @property
    def device(self) -> spy.Device:
        """Get the Slang device used by this package manager.

        :return: The Slang device instance.
        """
        return self._device

    @property
    def module_map(self) -> Dict[str, spy.Module]:
        """Get the module map containing the built Slang modules for each registered package.

        :return: A dictionary mapping package names to their corresponding Slang modules.
        """
        return self._module_map

    @staticmethod
    def register_package(package_cls: type[SlangPackage]) -> None:
        """Register a Slang package class.

        :param package_cls: The SlangPackage class to register
        :raises ValueError: If a package with the same name is already registered.
        """
        package_name = package_cls.name()
        if package_name in packages:
            raise ValueError(
                f"A package with the name '{package_name}' is already registered."
            )
        packages[package_name] = package_cls

    def _sort_packages_by_dependencies(self) -> List[type[SlangPackage]]:
        """Topologically sort the registered packages based on their dependencies.

        :return: A list of SlangPackage classes sorted in the order they should be built.
        """
        n = len(packages)
        in_degree = {name: 0 for name in packages}
        dependents = {name: [] for name in packages}
        queue = deque()
        sorted_packages = []

        # Calculate in-degrees based on dependencies
        for package_cls in packages.values():
            for dep in package_cls.dependencies():
                dep_name = dep.name()
                if dep_name not in packages:
                    raise ValueError(
                        f"Package '{package_cls.name()}' depends on unregistered package '{dep_name}'."
                    )
                in_degree[package_cls.name()] += 1
                dependents[dep_name].append(package_cls.name())

        # Kahn's algorithm for topological sorting
        for name, degree in in_degree.items():
            if degree == 0:
                queue.append(name)

        while queue:
            current = queue.popleft()
            sorted_packages.append(packages[current])
            for dependent in dependents[current]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Check for cycles (if sorted_packages doesn't contain all packages, there is a cycle)
        if len(sorted_packages) != n:
            logger.error(
                "Cyclic dependency detected among packages. Registered packages: %s",
                list(packages.keys()),
            )
            raise ValueError("Cyclic dependency detected among packages.")

        return sorted_packages

    def _get_shader_paths(self) -> List[str]:
        """Get the shader paths from all registered packages.

        :return: A list of shader file paths from all registered packages.
        """
        shader_paths = []
        for package_cls in packages.values():
            shader_paths.extend(package_cls.shader_paths())
        return shader_paths
