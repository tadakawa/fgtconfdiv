from tkinter.filedialog import askopenfilenames
from pathlib import Path


class Config:
    option = dict(encoding="ascii", errors="surrogateescape")

    def __init__(self, fname):
        self.file = Path(fname)
        self.rows = self.file.read_text(**self.option).splitlines(keepends=True)

    def write(self, section: str, from_: int, to: int):
        output = self.file.with_name(f"{self.file.stem}_{section}.txt")
        output.write_text("".join(self.rows[from_:to]), **self.option)

    @property
    def name(self):
        return self.file.name

    def __iter__(self):
        return iter(self.rows)


def main():
    filenames = askopenfilenames(
        title="Fortigateのコンフィグファイルを選択してください",
        filetypes=[("config log file", "*.conf;*.log")],
        initialdir=".",
    )

    for config in map(Config, filenames):
        section = "header"
        vdom = ""
        nested = from_ = 0

        print(f"==  {config.name}  ".ljust(79, "="))
        for index, text in enumerate(config):
            text = text.rstrip()

            if text in ["config vdom", "config global"]:
                nested += 1
                section = text
                from_ = index
            elif text.startswith("config "):
                nested += 1
            elif text.startswith("edit "):
                nested += 1
                vdom = text[5:]
            elif text in ["next", "end"]:
                nested -= 1
            elif text == "":
                # ファイル出力
                if nested:
                    nested = 0
                    section = vdom
                to = index + 1
                print(f"{section=!r:16}: from {from_ + 1:7,} to {to:7,}")
                config.write(section, from_, to)


if __name__ == "__main__":
    main()
