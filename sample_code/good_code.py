"""Good code example with proper structure and documentation."""


class DataProcessor:
    """A class for processing and analyzing data."""

    def __init__(self, data):
        """
        Initialize the DataProcessor.
        
        Args:
            data: List of numeric values to process
        """
        self.data = data
        self.results = []

    def calculate_average(self):
        """
        Calculate the average of the data.
        
        Returns:
            The mean value of all data points, or 0 if no data
        """
        if not self.data:
            return 0
        return sum(self.data) / len(self.data)

    def filter_positive_values(self):
        """
        Filter and return only positive values from the data.
        
        Returns:
            List of positive values from the original data
        """
        positive_values = [value for value in self.data if value > 0]
        return positive_values
