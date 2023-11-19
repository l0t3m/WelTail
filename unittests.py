import unittest, os, sqlite3
import functions, db



class Test_db(unittest.TestCase):
    def setUp(self):
        self.fileName = "weltail.db"
        self.testSql = "SELECT * FROM users"
        self.testFileName = "newDB.db"

        if os.path.exists(self.fileName) == False:
            db.setup(filename=self.fileName)
        else:
            os.remove(self.fileName)
            db.setup(filename=self.fileName)
    
    def tearDown(self):
        if os.path.exists(self.fileName) == True:
            os.remove(self.fileName)
    
    def test_setup(self):
        os.remove(self.fileName)
        self.assertFalse(os.path.exists(self.fileName))
        db.setup()
        self.assertTrue(os.path.exists("weltail.db"))
        os.remove("weltail.db")
    
    def test_setup_newFileName(self):
        db.setup(filename=self.testFileName)
        self.assertTrue(os.path.exists(self.testFileName))
        os.remove(self.testFileName)

    def test_setup_existingFile(self):
        self.assertTrue(os.path.exists(self.fileName))
        db.setup(filename=self.fileName)
    
    def test_setup_TestData_true(self):
        db.setup(filename=self.testFileName, testData=True)
        data = db.query(sql=self.testSql, filename=self.testFileName)

        self.assertEqual(len(data['rows']), 1)
        os.remove(self.testFileName)
    
    def test_setup_TestData_false(self):
        db.setup(filename=self.testFileName, testData=False)
        data = db.query(sql=self.testSql, filename=self.testFileName)
        
        self.assertEqual(len(data['rows']), 0)
        os.remove(self.testFileName)



    def test_query(self):
        data = db.query(sql=self.testSql, filename=self.fileName)
        self.assertEqual(len(data), 2)
        self.assertTrue(isinstance(data, dict))
        self.assertTrue(isinstance(data['rows'], list))

    def test_query_wrongParameters(self):
        wrongSql = "SELECT * FROM none"
        wrongFile = "wrongFile.db"

        with self.assertRaises(sqlite3.OperationalError):
            db.query(sql=wrongSql, filename=self.fileName)
            db.query(sql=self.testSql, filename=wrongFile)








if __name__ == '__main__':
    unittest.main()