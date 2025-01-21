import requests
from bs4 import BeautifulSoup
import json


json_data = {}
def parse_hockey_matches(url):

    try:
        response = requests.get(url)
        response.raise_for_status()

        # to use correct encoding
        response.encoding = response.apparent_encoding


        soup = BeautifulSoup(response.text, "html.parser")


        match_cards = soup.find_all("div", class_="match-card calendar")
        matches = []



        for card in match_cards:

            versus_div = card.find("div", class_="match-versus calendar desktop calendar-future")
            if not versus_div:
                continue  # Skip if no team info is available
            teams = versus_div.text.replace("\xa0", " ").strip()



            date_div = card.find("div", class_="calendar-match-info-when calendar-future mobile")
            date = date_div.text.strip() if date_div else "Unknown Date"
            json_data[date] = []


            time_div = card.find("div", class_="calendar-match-info-time")


            time = time_div.text.strip() if time_div else "Unknown Time"



            ticket_button = card.find("a", href=True)
            ticket_url = ticket_button["href"] if ticket_button else "No Ticket Link"
            json_data[teams] = []




            matches.append({
                "teams": teams,
                "date": date,
                "time": time,
                "ticket_url": ticket_url
            })

        return matches



    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    except Exception as e:
        print(f"Error parsing the page: {e}")
        return []





def main():
    feed = 'schedule.asp?season=2025HUM&where=vsech'
    url = f'https://hchumo.uz/{feed}'

    matches = parse_hockey_matches(url)


    for match in matches:
        print(f"Teams: {match['teams']}")
        print(f"Date: {match['date']}")
        print(f"Time: {match['time']}")
        print(f"Ticket URL: {match['ticket_url']}")
        print("-" * 40)



if __name__ == '__main__':
    main()



with open('matches.json', mode='w', encoding='UTF-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)
