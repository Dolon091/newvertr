from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import requests
from bs4 import BeautifulSoup

class SubstApp(App):
    def build(self):
        # Set up the main layout
        layout = BoxLayout(orientation='vertical')

        # Get data from the function
        url_to_scrape = "https://www.gks-berlin.de/wp-content/uploads/Vertretungsplan/Monitor/SuS/subst_001.htm"
        column_name_to_find = "Klasse(n)"
        value_to_find = "11"
        data = self.get_lines_with_value_and_info(url_to_scrape, column_name_to_find, value_to_find)

        # Display data in labels
        for item in data:
            label = Label(text=item, size_hint_y=None, height=44)
            layout.add_widget(label)

        return layout

    def get_lines_with_value_and_info(self, url, column_name, value):
        try:
            # Send a GET request to the website
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract and append the date information
                date_element = soup.find('div', {'class': 'mon_title'})
                data = [f"Date: {date_element.text.strip()}\n"] if date_element else []

                # Extract and append messages from the table with class 'info'
                info_table = soup.find('table', {'class': 'info'})
                if info_table:
                    messages = info_table.find_all('td', {'class': 'info'})
                    data.extend([f"Message: {message.text.strip()}\n" for message in messages])

                # Find all <tr> elements where the specified column has the specified value
                lines_with_value = []
                for line in soup.find_all('tr', {'class': ['list', 'odd']}):
                    # Find all <td> elements within the current line
                    cells = line.find_all('td', {'class': 'list', 'align': 'center'})

                    # Check if the column "Klasse(n)" (assuming it's the second column) has the specified value
                    if len(cells) > 1 and cells[1].text.strip() == value:
                        # Extract and concatenate the text content of each <td> element with spaces
                        line_text = ' '.join(cell.text.strip() for cell in cells)
                        lines_with_value.append(line_text)

                # Append the full lines with spaces between columns
                data.extend([f"{line}\n" for line in lines_with_value])

                return data

            else:
                return [f"Failed to retrieve data. Status code: {response.status_code}"]

        except Exception as e:
            return [f"An error occurred: {e}"]

# Run the Kivy application
if __name__ == '__main__':
    SubstApp().run()