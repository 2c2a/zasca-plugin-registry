import json
import subprocess
import re


def main():
    with open("plugins.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    plugins = data.get("plugins", {})
    changed = False

    for plugin_id, info in plugins.items():
        repo_url = info.get("repository", "")
        if not repo_url:
            continue

        match = re.search(r"github\.com/([^/]+/[^/]+)", repo_url)
        if not match:
            continue

        repo = match.group(1).rstrip("/")
        version = None

        try:
            result = subprocess.run(
                ["gh", "api", "-q", ".tag_name",
                 f"repos/{repo}/releases/latest"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0 and result.stdout.strip():
                version = result.stdout.strip()
        except Exception:
            pass

        if not version:
            try:
                result = subprocess.run(
                    ["gh", "api", "-q", ".[0].name",
                     f"repos/{repo}/tags"],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0 and result.stdout.strip():
                    version = result.stdout.strip()
            except Exception:
                pass

        if not version:
            try:
                result = subprocess.run(
                    ["gh", "api", "-q", ".default_branch",
                     f"repos/{repo}"],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0 and result.stdout.strip():
                    branch = result.stdout.strip()
                    result2 = subprocess.run(
                        ["gh", "api", "-q", ".object.sha",
                         f"repos/{repo}/git/refs/heads/{branch}"],
                        capture_output=True, text=True, timeout=15
                    )
                    if result2.returncode == 0 and result2.stdout.strip():
                        version = result2.stdout.strip()[:7]
            except Exception:
                pass

        current = info.get("version", "N/A")
        if version and version != current:
            info["version"] = version
            changed = True
            print(f"[{plugin_id}] {current} -> {version}")
        else:
            print(f"[{plugin_id}] no update (current: {current})")

    with open("plugins.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open("/tmp/changed", "w") as f:
        f.write("1" if changed else "0")


if __name__ == "__main__":
    main()
