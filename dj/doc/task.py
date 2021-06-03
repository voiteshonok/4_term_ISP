class Task():
    def __init__(self, slug_name, path_to_input, path_to_expected_output, time_limit, memory_limit) -> None:
        self.slug_name = slug_name
        self.path_to_input = path_to_input
        self.path_to_expected_output = path_to_expected_output
        self.time_limit = time_limit
        self.memory_limit = memory_limit