from flask import Flask, render_template, request
from engine import EventRecommendation
import csv


app = Flask(__name__)
# Create an instance of the EventRecommendation class using your data file
event_recommendation = EventRecommendation('dataset.csv')

def load_event_data():
    event_data = []
    with open('dataset.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        # Skip the header row
        next(csv_reader, None)

        for row in csv_reader:
            event_data.append(row)
    return event_data

# Step 1: Define a function to recommend events
def recommend_events(user_id, event_type_filter=None, registration_required_filter=None):
    # Load event data from the CSV file
    event_data = load_event_data()

    # Filter events based on user input
    recommended_events = []

    for event in event_data:
        # Apply filters if provided
        if event_type_filter and event['EventType'] != event_type_filter:
            continue

        if registration_required_filter and event['RegistrationRequired'] != registration_required_filter:
            continue

        # Convert relevant fields to appropriate data types
        event['TicketPrice'] = float(event['TicketPrice'])

        # Handle 'FeedbackRating' conversion
        try:
            event['FeedbackRating'] = float(event['FeedbackRating'])
        except ValueError:
            # Set a default value (e.g., 0) when conversion fails
            event['FeedbackRating'] = 0

        # Handle 'TotalRevenue' conversion
        try:
            event['TotalRevenue'] = float(event['TotalRevenue'])
        except ValueError:
            # Set a default value (e.g., 0) when conversion fails
            event['TotalRevenue'] = 0

        event['Expenses'] = float(event['Expenses'])
        event['ProfitLoss'] = float(event['ProfitLoss'])
        event['SocialMediaPresence'] = event['SocialMediaPresence'].lower() == 'true'
        event['COVID19SafetyMeasures'] = event['COVID19SafetyMeasures'].lower() == 'true'
        event['COVID19CasesLinked'] = event['COVID19CasesLinked'].lower() == 'true'
        event['AcademicEvent'] = event['AcademicEvent'].lower() == 'true'
        event['ResearchPapersPresented'] = event['ResearchPapersPresented'].lower() == 'true'

        # Include the 'TopicsCovered' column as a list
        event['TopicsCovered'] = event['TopicsCovered'].split(', ')

        recommended_events.append(event)

    # Sort events by date in ascending order
    recommended_events.sort(key=lambda x: x['EventDate'])

    return recommended_events


# Step 2: Create a route to display recommended events
@app.route('/recommendations', methods=['POST'])
def recommend():
    # Get user inputs from the form
    user_id = request.form.get('user_id')
    event_type_filter = request.form.get('event_type')
    registration_required_filter = request.form.get('registration_required')

    # Get recommended event IDs using the event_recommendation instance
    recommended_event_ids = event_recommendation.make_recommendations(user_id)

    # Filter events based on user input using the event_recommendation instance
    filtered_events = event_recommendation.filter_events(event_type_filter, registration_required_filter)

    # Get details for recommended events
    recommended_events = [event_recommendation.get_event_details(event_id) for event_id in recommended_event_ids]

    # Render the recommend.html template and pass the recommended events
    return render_template('recommend.html', recommended_events=recommended_events)

# Default route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
