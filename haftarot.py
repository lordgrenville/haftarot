import pandas as pd

haf = pd.read_csv("haftarot.csv")

haf.columns = ["day", "book", "chapter"]

haf["book_"] = np.nan
haf["book_"] = haf["book_"].astype(str)
haf.loc[haf.book.str.contains("מלכים"), "book_"] = "מלכים"
haf.loc[haf.book.str.contains("שמואל"), "book_"] = "שמואל"
haf.loc[
    haf.book.isin(["הושע", "זכריה", "עמוס", "מלאכי", "עובדיה", "מיכה", "יונה"]), "book_"
] = "תרי עשר"
haf.loc[haf.book_.eq("nan"), "book_"] = np.nan
haf.book_ = haf.book_.fillna(haf.book)

haf["book_length"] = haf.book.map(
    {
        "הושע": 14,
        "זכריה": 14,
        "יהושע": 24,
        "יונה": 4,
        "יחזקאל": 48,
        "ירמיהו": 52,
        "ישעיהו": 66,
        "מיכה": 6,
        "מלאכי": 3,
        "מלכים א": 20,
        "מלכים ב": 25,
        "עובדיה": 1,
        "עמוס": 8,
        "שופטים": 21,
        "שמואל א": 30,
        "שמואל ב": 23,
    }
)

s = haf.book.value_counts().reset_index()
haf["book_count"] = haf["book"].map(dict(zip(s["book"], s["count"])))

s = haf.book_.value_counts().reset_index()
haf["book__count"] = haf["book_"].map(dict(zip(s["book_"], s["count"])))

s = haf.groupby("book_")["book_length"].unique().apply(lambda x: sum(x)).reset_index()
haf["book__length"] = haf["book_"].map(dict(zip(s["book_"], s["book_length"])))

haf["book_ratio"] = haf["book_count"].div(haf["book_length"])
haf["book__ratio"] = haf["book__count"].div(haf["book__length"])

# with kings I/II etc separated, and Trei Asar
(
    haf.rename({"book": "Book"}, axis=1)
    .groupby("Book")[["book_count", "book_length", "book_ratio"]]
    .max()
    .sort_values(by="book_ratio", ascending=False)
    .rename(
        {
            "book_count": "Number of Haftarot",
            "book_length": "Number of Chapters",
            "book_ratio": "Haftarot:Chapter ratio",
        },
        axis=1,
    )
    .style.format(
        {
            "Number of Haftarot": "{:n}",
            "Number of Chapters": "{:n}",
            "Haftarot:Chapter ratio": "{:.3}",
        }
    )
)

# ...and then without that
(
    haf.rename({"book_": "Book"}, axis=1)
    .groupby("Book")[["book__count", "book__length", "book__ratio"]]
    .max()
    .sort_values(by="book__ratio", ascending=False)
    .rename(
        {
            "book__count": "Number of Haftarot",
            "book__length": "Number of Chapters",
            "book__ratio": "Haftarot:Chapter ratio",
        },
        axis=1,
    )
    .style.format(
        {
            "Number of Haftarot": "{:n}",
            "Number of Chapters": "{:n}",
            "Haftarot:Chapter ratio": "{:.3}",
        }
    )
)
