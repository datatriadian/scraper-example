import httpx
from bs4 import BeautifulSoup


class ScraperError(Exception):
    pass


def main() -> None:
    url = "https://aws.amazon.com/ec2/faqs/"
    response = httpx.get(url)

    # 200 will be returned if the page loaded. If not something went wrong
    if response.status_code != 200:
        raise ScraperError(f"Error getting {url}. Status code {response.status_code} returned")

    soup = BeautifulSoup(response.text, "html.parser")
    div = soup.find_all("div", class_="lb-grid")

    for _ in range(4):  # The last 4 lb-grids aren't questions so remove them
        div.pop()

    ps = []

    # Go through all the divs and get the p tags. extend is used here to flatten the list
    for d in div:
        ps.extend(d.find_all("p"))

    info = []
    faq = []

    for p in ps[3:]:  # The first 3 aren't questions so skip them
        if p.text[:2] in ["Q:", "Q."]:  # If the text starts with Q: or Q. it is the question
            faq = [p.text.strip()]

        # Answers can be split across multiple p elements. This next part combines them together
        elif len(faq) == 1:
            faq.append(p.text.strip())
        else:
            faq[1] = f"{faq[1]} {p.text.strip()}"

        # Sometimes the question is actually a header and not a questions so ignore it if there is
        # no answer. If the length is > 1 that means an answer is present so append it to the info.
        if len(faq) > 1:
            info.append(tuple(faq))

    for i in info:
        print(i)


if __name__ == "__main__":
    main()
