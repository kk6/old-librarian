import more_itertools
import requests
from config.database import db
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry


def fetch_isbn_list():
    res = requests.get("https://api.openbd.jp/v1/coverage")
    return res.json()


def fetch_book_data(session, isbn_list):
    isbn_csv = ",".join(isbn_list)
    res = session.get(f"https://api.openbd.jp/v1/get?isbn={isbn_csv}")
    return res.json()


def create_retry_session(
    retry_total=5, backoff_factor=1, status_forcelist=(500, 502, 503, 504)
):
    s = requests.Session()
    retries = Retry(
        total=retry_total,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s


def main():
    db.table("summaries").delete()

    all_isbn_list = fetch_isbn_list()
    books_total = len(all_isbn_list)

    chunked_isbn_list = more_itertools.chunked(all_isbn_list, 1000)

    session = create_retry_session()

    with tqdm(total=books_total) as progress_bar:
        progress_bar.set_description("Downloading book summary")

        for isbn_list in chunked_isbn_list:
            data = fetch_book_data(session, isbn_list)
            # db.table("summaries").insert([book["summary"] for book in data])
            # progress_bar.update(len(isbn_list))
            for d in data:
                try:
                    db.table("summaries").insert(d["summary"])
                except Exception:
                    # TODO: Error log
                    pass
                progress_bar.update(1)


if __name__ == "__main__":
    main()
