import os
import requests


def GetAirbnb(location, checkin, checkout, adults):

    url = "https://airbnb13.p.rapidapi.com/search-location"

    rapid_api_key = os.environ.get("RAPID_API_KEY")

    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "airbnb13.p.rapidapi.com",
        "User-agent": "AirBnb"

    }

    querystring = {"location": location, "checkin": checkin, "checkout": checkout, "adults": adults,
                   "children": "0", "infants": "0", "pets": "0", "page": "1", "currency": "USD"}

    response = requests.get(url, headers=headers, params=querystring)

    response_json = response.json()

    # print(response_json)
    # Filter listings with a rating greater than 4.5 and extract the desired details
    filtered_listings = []
    # Initialize a counter for the entries
    entries_count = 0

    # Iterate over the results in the JSON response
    for listing in response_json['results']:
        # Check if the listing's rating is greater than 4.5
            # Add the listing's details to the filtered_listings list
        if 'rating' in listing and listing['rating'] > 4.5:
            filtered_listings.append({
                'name': listing['name'],
                'bathrooms': listing['bathrooms'],
                'beds': listing['beds'],
                'bedrooms': listing['bedrooms'],
                'persons': listing['persons'],
                'reviewsCount': listing['reviewsCount'],
                'rating': listing['rating'],
                'type': listing['type'],
                'address': listing['address'],
                'previewAmenities': listing['previewAmenities'],
                # Assuming total price is required
                'price': listing['price']['total'],
                'url': listing['url']
            })
            # Increment the counter
            entries_count += 1
            # Check if we have reached 5 entries
            if entries_count == 5:
                # Break the loop if 5 entries are collected
                break
        else:
            continue

    # print(f"\nTop Five Airbnb Listings in {location}: \n")
    result = f"\nTop Five Airbnb Listings in {location}: \n"
    for listing in filtered_listings:
        result += (f"\n🏠 Name: {listing['name']}\n🛁 Bathrooms: {listing['bathrooms']}\n🛏️ Beds: {listing['beds']}"
            f"\n🚪 Bedrooms: {listing['bedrooms']}\n👥 Persons: {listing['persons']}\n📝 Reviews Count: {listing['reviewsCount']}"
            f"\n⭐ Rating: {listing['rating']}\n🏡 Type: {listing['type']}\n📍 Address: {listing['address']}"
            f"\n🔑 Preview Amenities: {', '.join(listing['previewAmenities'])}\n💲 Price: ${listing['price']}"
            f"\n🔗 URL: {listing['url']}\n" + "-"*80)

    print(result)
    return result

# GetAirbnb("Islamabad", "2024-03-21", "2024-03-21", 1)

