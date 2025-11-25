import pandas as pd
import json
import os
import zipfile


class Reader:
    def __init__(self):
        pass

    def read_file(self, path: str) -> pd.DataFrame:

        self.path = path
        # path to dir
        self.path_to_dir: str = os.path.split(path)[0]
        # file full name
        self.file_full_name: str = os.path.split(path)[1]
        # file name
        self.file_name: str = os.path.splitext(self.file_full_name)[0]
        # file extension
        self.file_extension: str = os.path.splitext(self.file_full_name)[1]

        match self.file_extension:
            case ".xlsx":
                return pd.read_excel(self.path, names=["text"])
            case ".json":
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return pd.DataFrame(data, columns=["text"])
            case ".csv":
                return pd.read_csv(self.path)
            case ".zip":
                return self.read_zip_file(self.path)
            case ".txt":
                with open(self.path, "r", encoding="utf-8") as f:
                    data = f.read()
                return pd.DataFrame(data.split("\n"), columns=["text"])
            case _:
                return pd.DataFrame(columns=["text"])

    def read_zip_file(self, path: str) -> pd.DataFrame:

        zip_file_path = path

        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            data = ""
            df_data = pd.DataFrame(columns=["text"])
            for name in zip_ref.namelist():
                if name.endswith(".txt"):
                    with zip_ref.open(name) as file:
                        data += file.read().decode("utf-8")
                if name.endswith(".csv"):
                    with zip_ref.open(name) as file:
                        df_data = pd.concat(df_data, pd.read_csv(file))

        if data:
            return pd.DataFrame(data.split("\n"), columns=["text"])
        else:
            return df_data
