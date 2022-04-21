from django.db import models

class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> list:
        distribution = [[(True  if self.passengers > ((b*2)+a) else False) for a in range(2)] for b in range(int(self.vehicle_type.max_capacity/2))]
        return distribution

    def validate_number_plate(plate) -> bool:
        result = True
        try:
            plate_pair=plate.split("-")
            if plate_pair[0].isnumeric() or plate_pair[1].isalpha() or  plate_pair[2].isalpha():
                result = False
        except:
            result = False
        return result


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self) -> bool:
        return True if self.end else False  
