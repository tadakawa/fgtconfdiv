import tkinter
import tkinter.filedialog as fd
from pathlib import Path


def main():
    tkinter.Tk().withdraw()
    title = "Fortigateのコンフィグファイルを選択してください"
    ftypes = [("ログファイル", "*.conf;*.log")]
    if not (
        filenames := fd.askopenfilenames(title=title, filetypes=ftypes, initialdir=".")
    ):
        return

    for file in (Path(filename) for filename in filenames):
        print(f"==  {file.name}  ".ljust(79, "="))
        with file.open() as f:
            data = f.readlines()

        indent = 0
        start_index = 0
        name = ""
        for i, text in enumerate(data):
            text = text.rstrip()
            if text == "config vdom":
                indent = 0
                start_index = i
            elif text.startswith("config"):
                indent += 1
                if text == "config global":
                    start_index = i
                    name = "global"
            elif text.startswith("edit "):
                indent += 1
                if indent == 1:
                    name = text.rstrip().replace("edit ", "")
            elif text.startswith(("next", "end")):
                indent -= 1
                if indent == 0:
                    print(f"{name=:6}: from {start_index + 1:6} to {i + 1:6}")
                    with file.with_suffix("." + name + ".txt").open("wt") as f:
                        f.writelines(data[slice(start_index, i+1)])
                elif indent < 0:
                    indent = 0


if __name__ == "__main__":
    main()
