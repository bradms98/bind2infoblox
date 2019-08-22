class b2i():
    def __init__(self, bindInput):
        if not bindInput:
            self.bindInput = 'Default Input'
        self.csvOutput = bindInput + ' ' + bindInput
