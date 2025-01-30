from requests import Session


# https://www.linkedin.com/voyager/api/graphql
# ?variables=(
#   start:25,
#   count:10,
#   jobPosting:urn:li:fsd_jobPosting:4000865419,
#   sortType:RELEVANCE,
#   sortOrder:DESCENDING
# )&
# queryId=voyagerHiringDashJobApplications.843c8c719ed6c86c0030f93ba366e2f0

class LinkedinScraper:

    def __init__(self, url: str):
        self._url = url
        self._cookies = {}

    def _fetch_cookies(self, session: Session) -> dict[str,str]:
        session.get(self._url)
        self._cookies = session.cookies.get_dict()
        return self._cookies

    def _build_graphql(self):
        id = "4000865419"
        base = "https://www.linkedin.com/voyager/api/graphql"
        variables = [
            f"start:{0}",
            f"count:{10}",
            f"jobPosting:urn:li:fsd_jobPosting:{id}",
            "sortType:RELEVANCE",
            "sortOrder:DESCENDING"
        ]
        query_id = "voyagerHiringDashJobApplications.843c8c719ed6c86c0030f93ba366e2f0"
        return f"{base}?variables=({','.join(variables)})&queryId={query_id}"


    def scrape(self) -> list[str]:
        session = Session()
        cookies = self._fetch_cookies(session)
        graphql = self._build_graphql()

        session.cookies.set('bcookie',"v=2&eddf33ee-814b-4030-8885-8147435a51ee")
        session.cookies.set('bscookie',"v=1&2023073012560834312d66-220d-4c15-8323-cf40f7468db8AQG5DO-Oqoqg6QvGM-nzZmCUymC5UvaB")
        session.cookies.set('dfpfpt',"61365fb543a44c048b0e52087289e721")

        response = session.get(graphql)
        print(response)