class ErrorManager(Exception):
    """
    Responsible for controlling system errors.
    """

    def __init__(self, message: str, error_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def get_error_description(self) -> str:
        """
        Method responsible for getting error
        description
        """
        description = (
            f"Message: {self.message}.\n" + f"Error Code: {self.error_code}."
        )

        return description
