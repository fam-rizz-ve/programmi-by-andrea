class figura:
    def __init__(self,):
        self._area = 0
    def area(self):
        print(self.area)
class quadrato(figura):
    def __init__(self,lato):
        super().__init__()
        self.lato = lato
    def area(self):
        self._area = self.lato ** 2
        super().area()
class cerchio(figura):
    def __init__(self,raggio):
        super().__init__()
        self.raggio = raggio
    def area(self):
        self._area = (self.raggio ** 2) * 3.14
        super().area()
quadrato1 = quadrato(5)
cerchio1 = cerchio(4)
quadrato1.area()
cerchio1.area()