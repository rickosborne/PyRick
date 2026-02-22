from datetime import datetime, timezone
from sys import argv

from semver import Version

version_file = "packages/__version__.py"

today = datetime.now(timezone.utc)
today_semver = Version(today.year, today.month, today.day)

toml_for_path = dict[str, dict[str, object]]()


with open(version_file, "r", encoding="utf-8") as input:
    line = input.readline().strip()
    print(f"Version file: {line}")

print(f"Today: v{today_semver}")

package_paths = {"vote": "packages/rickosborne_vote/pyproject.toml"}

package_versions = {"vote": Version.parse("TODO")}

next_semver = today_semver

for pkg_name, sv in package_versions.items():
    print(f"{pkg_name}: v{sv} ({package_paths[pkg_name]})")
    if sv >= next_semver:
        next_semver = sv.bump_minor()

print(f"Next: v{next_semver}")

if "--commit" in argv:
    with open(version_file, "w", encoding="utf-8") as out:
        out.writelines([f'__version__ = "{next_semver}"'])
    print(f"✏️ Updated {version_file}")
else:
    print("Dry run.  Nothing changed.")
