

class TopicSerializer:
    def __init__(self, row_data=None):
        """
        :param row_data: response from the databse
        """
        self.row_data = row_data

    def to_dict(self):
        if not self.row_data:
            return None

        id, name, description = self.row_data

        return {
            'id': id,
            'name': name,
            'description': description
        }