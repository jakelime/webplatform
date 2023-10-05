from datetime import datetime
import git
from pathlib import Path

def get_time(datetimestrformat: str = "%Y%m%d_%H%M%S", append_microseconds=False):
    """
    Returns the datetime string at the time of function call
    :param datetimestrformat: datetime string format, defaults to "%Y%m%d_%H%M%S"
    :type datetimestrformat: str, optional
    :return: datetime in string format
    :rtype: str
    """
    now = datetime.now()
    time_str = now.strftime(datetimestrformat)
    if append_microseconds:
        time_str_ms = now.strftime("%f")[:2]
        time_str = f"{time_str}{time_str_ms}"
    return time_str


def get_latest_git_tag(base_dir):
    """function to use GitPython to get a list of tags

    :param base_dir: same path as settings.py BASE_DIR
    :type base_dir: str
    :return: latest git tag
    :rtype: str
    """
    repo_path = base_dir.parent
    repo = git.Repo(repo_path)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    if not tags:
        return "NoGitTagsFound"
    else:
        latest_tag = tags[-1]
        return str(latest_tag)


def main():
    basedir = Path(__file__).parent.parent
    ver = get_latest_git_tag(basedir)
    # print(f"Git tag retreived: {ver=}")

if __name__ == "__main__":
    main()