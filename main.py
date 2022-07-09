#!/usr/bin/env python3


import fetch
import requests
import zipfile
import os
import glob
import json


HOME = os.getenv("HOME")


def download_artifacts(res: dict, path: str) -> None:
    for i in res["launchTypeData"]["artifacts"]:
        with open(f"{path}/{i['name']}", "wb") as f:
            print(f"Downloading {i['name']}...")
            f.write(requests.get(i["url"]).content)

    with zipfile.ZipFile(glob.glob(f"{path}/natives-*.zip")[0], "r") as zip_ref:
        print("Extracting Natives...")
        zip_ref.extractall(f"{path}/natives")


def launch(jvm_path: str, path: str, config: dict) -> None:
    extra_args = [
        "--add-modules",
        "jdk.naming.dns",
        "--add-exports",
        "jdk.naming.dns/com.sun.jndi.dns=java.naming",
        f"-Djna.boot.library.path={path}/natives",
        f"-Djava.library.path={path}/natives",
        "-Dlog4j2.formatMsgNoLookups=true",
        "--add-opens",
        "java.base/java.io=ALL-UNNAMED",
    ]

    lunar_files = [
        f"{path}/{i.name}"
        for i in os.scandir(path)
        if i.is_file() and not i.name.endswith(".zip")
    ]

    os.system(
        f"{jvm_path} \
{' '.join(extra_args)} \
{' '.join(config['jvm_args'])} \
-cp {':'.join(lunar_files)} \
com.moonsworth.lunar.patcher.LunarMain \
--accessToken 0 \
--version 1.8 \
--assetIndex 1.8 \
--gameDir {config['game_dir']} \
--texturesDir {HOME}/.lunarclient/textures \
--width {config['width']} --height {config['height']} \
"
    )


def checksum(res: dict, path: str) -> bool:
    lc_sha1 = [i["sha1"] for i in res["launchTypeData"]["artifacts"]]
    current_sha1 = [
        os.popen(f"sha1sum {path}/{i.name} " + "| awk '{ print $1 }'").read().strip()
        for i in os.scandir(path)
        if i.is_file()
    ]

    if not os.path.exists(f"{path}/natives") or len(
        set(zip(lc_sha1, current_sha1))
    ) != len(lc_sha1):
        return True


def config() -> dict[str, int]:
    with open("config.json", "r") as f:
        f = json.load(f)

    return {
        "jvm_args": (f["jvm_args"]),
        "jvm_path": os.path.expandvars((f["jvm_path"])),
        "artifact_path": os.path.expandvars(f["artifact_path"]),
        "game_dir": os.path.expandvars(f["game_dir"]),
        "width": f["width"],
        "height": f["height"],
    }


def main(res: dict):
    path = config()["artifact_path"]
    jvm_path = config()["jvm_path"] or f"{HOME}/.lunarclient/jre/zulu17*/bin/java"

    if not os.path.exists(path):
        os.mkdir(path)

    if checksum(res, path):
        download_artifacts(res, path)

    launch(jvm_path, path, config())


if __name__ == "__main__":
    main(
        fetch.res,
    )
