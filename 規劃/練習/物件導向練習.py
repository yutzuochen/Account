class Car:
    # wheels_number:輪胎數量, car_doors:車門數量, passengers:乘客數量
    def __init__(self, wheels_number=4, car_doors=4, passengers=4):
        self.wheels_number = wheels_number
        self.car_doors = car_doors
        self.passengers = passengers
    def drive(self):
        print("Drive a car .Haaaaa")
 
# SUV也是一種車子，所以繼承Car
class SUV(Car):
    # brand_name:品牌名稱, air_bag:安全氣囊數, sunroof:是否擁有天窗
    def __init__(self, wheels_number, car_doors, passengers, brand_name="GG", air_bag=2, sunroof=False):
        super().__init__(wheels_number, car_doors, passengers)
        self.brand_name = brand_name
        self.air_bag = air_bag
        self.sunroof = sunroof
    # 覆寫父類別的drive
    def getDetails(self):
        print("==== Details ====")
        print("Wheels number:", self.wheels_number)# 可直接呼叫父類別的變數(屬性)
        print("Doors number:", self.car_doors)         # 可直接呼叫父類別的變數(屬性)
        print("Passengers:", self.passengers)
        print("Brand:", self.brand_name)
        print("Air-bags number:", self.air_bag)
        print("Sunroof:", self.sunroof)
        print("=================")

#car = Car()
#car.drive()

new = SUV(3,4,5)
new.drive()
