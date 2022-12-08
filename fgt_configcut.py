from __future__ import annotations

import collections
import tkinter
import tkinter.filedialog as fd
from pathlib import Path


class Config(collections.UserList[str]):
    @classmethod
    def read(cls, file: Path | str) -> Config:
        with Path(file).open() as f:
            return cls(f.readlines())

    def write(self, file: Path | str, from_: int, to_: int) -> None:
        with Path(file).open("wt") as f:
            f.writelines(self[from_:to_])


def main():
    tkinter.Tk().withdraw()
    title = "Fortigateのコンフィグファイルを選択してください"
    ftypes = [("ログファイル", "*.conf;*.log")]
    if not (
        filenames := fd.askopenfilenames(title=title, filetypes=ftypes, initialdir=".")
    ):
        return

    for filename in filenames:
        file = Path(filename)
        print(f"==  {file.name}  ".ljust(79, "="))
        data = Config.read(file)

        nested = 0
        start_idx = 0
        name = vdom_name = ""

        for idx, text in enumerate(data):
            text = text.rstrip()
            if text in ["config vdom", "config global"]:
                nested = 1
                name = vdom_name = text
                start_idx = idx
            elif text.startswith(("edit ", "config")):
                nested += 1
                if nested == 2 and text.startswith("edit "):
                    # 2階層目の "edit xxxx" は VDOM名として一時保存
                    vdom_name = text[5:]
            elif text in ["next", "end"]:
                nested -= 1
                if nested == 1 and text == "end":
                    # "edit VDOM名" セクションが "end" で終わったら name を更新
                    name = vdom_name
            elif text == "":
                nested = 0
                print(f"{name=:14}: from {start_idx + 1:6} to {idx + 1:6}")
                if name:
                    output_file = file.with_suffix("." + name + ".txt")
                else:
                    output_file = file.with_suffix(".txt")
                data.write(output_file, start_idx, idx + 1)


if __name__ == "__main__":
    main()
