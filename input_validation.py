

class ErrorHandling:

    def __init__(self):
        pass

    def validate_string_input(self, input):
        if not isinstance(input, str):
            raise ValueError("The input must be a string")
        if not input:
            raise ValueError("Input wasn't given")

        input = input.split(',')
        for i in input:
            try:
                if int(i) < 100 or int(i) > 990:
                    raise ValueError("Inputted postal codes were incorrect!")
            except ValueError:
                raise ValueError("Inputted postal codes were incorrect!")
        return True

    # def validate_integer_input(self, input):
    #     input = int(input)
    #     if input < 0:
    #         raise ValueError("The integer must be a positive number")
    #     if not isinstance(input, int):
    #         raise ValueError("The input must be an integer")
    #
    #     return True