import os
import ftplib

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

FTP_HOST = os.environ.get("FTP_HOST")
FTP_USERNAME = os.environ.get("FTP_USERNAME")
FTP_PASSWORD = os.environ.get("FTP_PASSWORD")
FTP_PATH = os.environ.get("FTP_PATH")


def ftp_connect() -> ftplib.FTP:
    return ftplib.FTP(
        host=FTP_HOST,
        user=FTP_USERNAME,
        passwd=FTP_PASSWORD
    )


def ftp_run() -> None:
    session = ftp_connect()

    try:
        session.mkd(FTP_PATH)
    except Exception:
        pass

    _file = open('index.html', 'rb')
    session.storbinary('STOR index.html', _file)

    for currentpath, folders, files in os.walk('blog'):
        host_path = currentpath.replace("blog", FTP_PATH)

        for folder in folders:
            path_folder = os.path.join(host_path, folder)
            print(f"---{path_folder}")

            try:
                session.mkd(path_folder)
            except Exception:
                pass

        for _file in files:
            path_file = os.path.join(currentpath, _file)
            host_file = os.path.join(host_path, _file)
            print(f"   |___{host_file}")

            try:
                _file = open(path_file, 'rb')
                session.storbinary(f'STOR {host_file}', _file)
            except Exception:
                pass


if __name__ == "__main__":
    ftp_run()
