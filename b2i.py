class b2i():
    def __init__(self, bindInput):
        self.bindInput = bindInput
        
        if not bindInput:
            self.bindInput = 'Default Input'
        self.csvOutput = bindInput + ' ' + bindInput
