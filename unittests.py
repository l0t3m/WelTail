import unittest, os, sqlite3
import functions, db



# class Test_db(unittest.TestCase):
#     def setUp(self):
#         self.fileName = "weltail.db"
#         self.testSql = "SELECT * FROM users"
#         self.testFileName = "newDB.db"

#         if os.path.exists(self.fileName) == True:
#             os.remove(self.fileName)
#         db.setup(filename=self.fileName)
    
#     def tearDown(self):
#         if os.path.exists(self.fileName) == True:
#             os.remove(self.fileName)
    
#     def test_setup(self):
#         os.remove(self.fileName)
#         self.assertFalse(os.path.exists(self.fileName))
#         db.setup()
#         self.assertTrue(os.path.exists("weltail.db"))
#         os.remove("weltail.db")
    
#     def test_setup_newFileName(self):
#         db.setup(filename=self.testFileName)
#         self.assertTrue(os.path.exists(self.testFileName))
#         os.remove(self.testFileName)

#     def test_setup_existingFile(self):
#         self.assertTrue(os.path.exists(self.fileName))
#         db.setup(filename=self.fileName)
    
#     def test_setup_TestData_true(self):
#         db.setup(filename=self.testFileName, testData=True)
#         data = db.query(sql=self.testSql, filename=self.testFileName)

#         self.assertEqual(len(data['rows']), 1)
#         os.remove(self.testFileName)
    
#     def test_setup_TestData_false(self):
#         db.setup(filename=self.testFileName, testData=False)
#         data = db.query(sql=self.testSql, filename=self.testFileName)
        
#         self.assertEqual(len(data['rows']), 0)
#         os.remove(self.testFileName)

#     def test_query(self):
#         data = db.query(sql=self.testSql, filename=self.fileName)
#         self.assertEqual(len(data), 2)
#         self.assertTrue(isinstance(data, dict))
#         self.assertTrue(isinstance(data['rows'], list))

#     def test_query_wrongParameters(self):
#         wrongSql = "SELECT * FROM none"
#         wrongFile = "wrongFile.db"

#         with self.assertRaises(sqlite3.OperationalError):
#             db.query(sql=wrongSql, filename=self.fileName)
#             db.query(sql=self.testSql, filename=wrongFile)
#             db.query(sql="abc", filename=self.fileName)
#             db.query(sql=self.testSql, filename="abc")

#     def test_get_TableKeys(self):
#         expected = ['user_id', 'username', 'fullname', 'password']
#         data = db.get_TableKeys()

#         self.assertTrue(isinstance(data, list))
#         self.assertEqual(len(expected), len(data))
#         self.assertEqual(data, expected)
    
#     def test_get_TableKeys_wrongParameters(self):
#         wrongSql = "SELECT * FROM none"
#         wrongFile = "wrongFile.db"

#         with self.assertRaises(sqlite3.OperationalError):
#             db.get_TableDicts(sql=wrongSql, filename=self.fileName)
#             db.get_TableDicts(sql=self.testSql, filename=wrongFile)

#     def test_get_TableDicts(self):
#         expected = [{'user_id': 1, 'username': 'lotem', 'fullname': 'lotem', 'password': '1212'}]
#         data = db.get_TableDicts()

#         self.assertTrue(isinstance(data, list))
#         self.assertEqual(len(data), 1)
#         self.assertEqual(data, expected)
    
#     def test_get_TableDicts_wrongParameters(self):
#         wrongSql = "SELECT * FROM none"
#         wrongFile = "wrongFile.db"

#         with self.assertRaises(sqlite3.OperationalError):
#             db.get_TableDicts(sql=wrongSql, filename=self.fileName)
#             db.get_TableDicts(sql=self.testSql, filename=wrongFile)



class Test_functions(unittest.TestCase):
    def setUp(self):
        self.fileName = "weltail.db"
        self.username = "lotem"
        self.user_id = 1
        self.pet_id = 1

        if os.path.exists(self.fileName) == True:
            os.remove(self.fileName)
        db.setup(filename=self.fileName)
    
    def tearDown(self):
        if os.path.exists(self.fileName) == True:
            os.remove(self.fileName)
    
    def test_getUserData(self):
        expected = {'user_id': 1, 'username': 'lotem', 'fullname': 'lotem', 'password': '1212'}
        data = functions.getUserData(username=self.username)

        self.assertEqual(len(data), len(expected))
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data, expected)
    
    def test_getUserData_testingParameters(self):
        expected = {'user_id': 1, 'username': 'lotem', 'fullname': 'lotem', 'password': '1212'}
        usernames = ["LOTEM", "Lotem", "loTEM"]

        for username in usernames:
            data = functions.getUserData(username=username)
            self.assertEqual(len(data), 4)
            self.assertTrue(isinstance(data, dict))
            self.assertEqual(data, expected)

    def test_getUserData_wrongParameters(self):
        expected = None
        usernames = [" ", "---", "1234", "!", "_test_", "newUser", 1234, [], {}]

        for username in usernames:
            data = functions.getUserData(username=username)
            self.assertEqual(data, expected)



    def test_getPetActivities(self):
        data = functions.getPetActivities(user_id=self.user_id, pet_id=self.pet_id)
        self.assertEqual(len(data), 1)
        self.assertTrue(isinstance(data, list))



if __name__ == '__main__':
    unittest.main()