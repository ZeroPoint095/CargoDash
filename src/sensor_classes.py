class Sensor:
    def __init__(self, sensor_type, value_type):
        # Sensor type is eg speed, force, distance, temperature, etc.
        # Value type is eg int, float, vector, analog signal.
        self.sensor_type = sensor_type
        self.value_type = value_type

    def read_sensor():
        sensor_value = None
        return sensor_value