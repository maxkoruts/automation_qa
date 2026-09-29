# task1
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


class Manager(Employee):
    def __init__(self, name, salary, department):
        Employee.__init__(self, name, salary)   # було: super().__init__(name, salary)
        self.department = department


class Developer(Employee):
    def __init__(self, name, salary, programming_language):
        Employee.__init__(self, name, salary)   # було: super().__init__(name, salary)
        self.programming_language = programming_language


class TeamLead(Manager, Developer):
    def __init__(self, name, salary, department, programming_language, team_size):
        Manager.__init__(self, name, salary, department)
        Developer.__init__(self, name, salary, programming_language)
        self.team_size = team_size

    def __repr__(self):
        return (f"TeamLead(name={self.name!r}, salary={self.salary}, "
                f"department={self.department!r}, "
                f"programming_language={self.programming_language!r}, "
                f"team_size={self.team_size})")


import unittest


class TestTeamLead(unittest.TestCase):
    def setUp(self):
        self.lead = TeamLead(
            name="Олена Ковальчук",
            salary=45000,
            department="R&D",
            programming_language="Python",
            team_size=5
        )

    def test_is_instance_of_both_parents(self):
        self.assertIsInstance(self.lead, Manager)
        self.assertIsInstance(self.lead, Developer)
        self.assertIsInstance(self.lead, Employee)

    def test_manager_attributes(self):
        self.assertTrue(hasattr(self.lead, "department"))
        self.assertEqual(self.lead.department, "R&D")

    def test_developer_attributes(self):
        self.assertTrue(hasattr(self.lead, "programming_language"))
        self.assertEqual(self.lead.programming_language, "Python")

    def test_employee_attributes(self):
        self.assertEqual(self.lead.name, "Олена Ковальчук")
        self.assertEqual(self.lead.salary, 45000)

    def test_own_attribute(self):
        self.assertTrue(hasattr(self.lead, "team_size"))
        self.assertEqual(self.lead.team_size, 5)


if __name__ == "__main__":
    unittest.main()