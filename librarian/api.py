import bocadillo
from models.summary import Summary

api = bocadillo.API()


@api.route("/")
async def index(req, res):
    res.html = await api.template("index.html")


@api.route("/search")
async def search(req, res):
    search_query = req.query_params.get("q", "")
    page = int(req.query_params.get("page", 1))
    if search_query:
        words = search_query.strip().split(" ")
        summaries = (
            Summary.or_where_in("isbn", words)
            .or_where_in("title", words)
            .or_where_in("publisher", words)
            .or_where_in("author", words)
            .order_by("title", "asc")
            .paginate(20, page)
        )
    else:
        summaries = Summary.order_by("title", "asc").paginate(20, page)
    res.html = await api.template(
        "search.html", summaries=summaries, q=search_query, page=page
    )


@api.route("/book/{isbn}")
async def book_detail(req, res, isbn):
    summary = Summary.where("isbn", isbn).first_or_fail()
    res.html = await api.template("book.html", summary=summary)


if __name__ == "__main__":
    api.run(debug=True)
