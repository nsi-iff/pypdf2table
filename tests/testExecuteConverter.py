import unittest
import os, sys
from pypdf2table.ExecuteConverter import ExecuteConverter
import shutil

class TestExecuteConverter(unittest.TestCase):

    def setUp(self):
        self.executeConverterObj = ExecuteConverter()

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testTableExtraction(self):
        self.outputdir = os.path.join(sys.path[0], 'extracted_tables')
        os.mkdir(self.outputdir)
        self.executeConverterObj.extractTables(os.path.join(sys.path[0],
                                               'files/premioprofessor.pdf'), self.outputdir)

        assert len(os.listdir(self.outputdir)) == 4, "Tables weren't extracted"


def suite():
    suite = unittest.makeSuite(TestExecuteConverter)
    return suite


if __name__ == '__main__':
    unittest.main()
