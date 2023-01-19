from os import path as _osPath, listdir as _listdir

def getSSLContext(path:str) -> tuple[str, str]:
    if not _osPath.exists(path):
        raise FileNotFoundError(f"Path {path} not found.")
    if not _osPath.isdir(path):
        raise NotADirectoryError(f"Path {path} is not a directory.")
    files = _listdir(path)
    filePem: str | None = None
    fileKey: str | None = None
    for file in files:
        if file.lower().endswith(".pem"):
            filePem = file
            break
    for file in files:
        if file.lower().endswith(".key"):
            fileKey = file
            break
    if filePem and fileKey:
        return filePem, fileKey
    else:
        raise FileNotFoundError("No pem or key file found.")