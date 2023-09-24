import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

class EventRecommendation:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)
        self.label_encoder = LabelEncoder()
        self.user_item_matrix = None
        self.model = None
        self.build_recommendation_model()

    def preprocess_data(self):
        # Encoding categorical variables
        self.data['EventType'] = self.label_encoder.fit_transform(self.data['EventType'])
        # Add more preprocessing steps if needed

    def build_recommendation_model(self):
        self.preprocess_data()
        # Assuming you want to build a collaborative filtering model
        user_item_matrix = pd.pivot_table(self.data, index='User ID', columns='Event ID', values='FeedbackRating', fill_value=0)
        self.model = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute', n_jobs=-1)
        self.model.fit(user_item_matrix)
        self.user_item_matrix = user_item_matrix  # Store user-item matrix

    def make_recommendations(self, user_id, k=5):
        # Your recommendation logic here
        # Example: Get the k-nearest neighbors and recommend items
        _, neighbor_indices = self.model.kneighbors([self.user_item_matrix.iloc[user_id]], n_neighbors=k + 1)
        # Return recommended event IDs
        return neighbor_indices[0][1:]

    def filter_events(self, event_type=None, registration_required=None):
        # Apply filters if needed
        filtered_data = self.data.copy()
        if event_type is not None:
            filtered_data = filtered_data[filtered_data['EventType'] == event_type]
        if registration_required is not None:
            filtered_data = filtered_data[filtered_data['RegistrationRequired'] == registration_required]
        return filtered_data

    def get_event_details(self, event_id):
        # Retrieve event details by event ID
        return self.data[self.data['Event ID'] == event_id].to_dict(orient='records')[0]

