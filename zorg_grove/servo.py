from zorg.driver import Driver


class Servo(Driver):

    def __init__(self, options, connection):
        super(Servo, self).__init__(options, connection)

        self.angle = -1
        self.commands += ["set_angle", "get_angle"]

    def set_angle(self, angle):
        """
        Set the angle of the servo motor.
        """
        self.angle = angle
        self.connection.servo_write(self.pin, angle)

    def get_angle(self):
        """
        Get the current angle of the servo motor.
        """
        return self.angle
