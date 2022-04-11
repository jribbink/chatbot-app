from datetime import datetime
import re
import sys
from filters.response_filter import ResponseFilter
from googleplaces import GooglePlaces as GooglePlacesAPI, types
import googlemaps


YOUR_API_KEY = sys.argv[2]

google_places = GooglePlacesAPI(YOUR_API_KEY)

gmaps = googlemaps.Client(key=YOUR_API_KEY)


class GooglePlaces(ResponseFilter):
    def parse(self, current_repsonse, original_response, query):
        special_queries = re.findall(r"\$\{(.*)\}", original_response)

        if "location.hospital" in special_queries:

            def response_function(user_response):
                try:
                    query_result = google_places.nearby_search(
                        location=user_response,
                        keyword="hospital",
                        radius=20000,
                        types=[types.TYPE_HOSPITAL],
                    )
                    result = query_result.places[0]
                    result.get_details()
                    ret = [
                        "The nearest hospital is {} at {}".format(
                            result.name, result.formatted_address
                        ),
                        "Would you like directions to this hospital?",
                    ]

                    def resp_directions_query(resp_directions):
                        if resp_directions.lower() not in [
                            "yes",
                            "yeah",
                            "maybe",
                            "possibly",
                            "yes, please",
                            "please",
                            "yes please",
                            "y",
                            "thanks",
                        ]:
                            return "Alright, good luck with your ailment"

                        now = datetime.now()
                        ret = "\n".join(
                            [
                                x["html_instructions"]
                                for x in gmaps.directions(
                                    user_response,
                                    result.formatted_address,
                                    mode="driving",
                                    departure_time=now,
                                )[0]["legs"][0]["steps"]
                            ]
                        )
                        return ret

                    self.request_response("\n".join(ret), resp_directions_query)
                except Exception as ex:
                    print(ex)
                    self.request_response(
                        "Sorry, I didn't quite understand that.  What is your current location?",
                        response_function,
                    )

            self.request_response("What is your current location?", response_function)

        return current_repsonse
