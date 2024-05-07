class Vehicle:

    compassHeading = 'NULL'


    def __init__(self, dirTag):
        self.dirTag = dirTag
        Vehicle.getCompassHeading(self)
    
    def getCompassHeading(self):
        if ('_0_' in self.dirTag):
            self.compassHeading = 'S'
        else:
            self.compassHeading = 'N'