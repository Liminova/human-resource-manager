from models import Person
import unittest

class TestPerson(unittest.TestCase):
    def test_create_person(self):
        person = Person("Rylie", "2003-08-22", "727", "0123456727", "Sleep")

        self.assertEqual(person.name, "Rylie")
        self.assertEqual(person.dob, "2003-08-22")
        self.assertEqual(person.id, "727")
        self.assertEqual(person.phone, "0123456727")
        self.assertEqual(person.department, "Sleep")

    def test_mutate_person(self):
        person = Person("Rylie", "2003-08-22", "727", "0123456727", "Sleep")

        self.assertEqual(person.id, "727")

        person.id = "420"

        self.assertEqual(person.id, "420")

if __name__ == "__main__":
    unittest.main()
