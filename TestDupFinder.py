import unittest
from dupfinder import DupFinder

class TestDupFinder(unittest.TestCase):
    """description of class"""

    def myAssertEquals(self, expected, actual):
        if expected == actual: return
       
        if isinstance(expected, unicode):
            strExpected = expected.encode('8859', 'replace')
        else:
            strExpected = str(expected)

        if isinstance(actual, unicode):
            strActual = actual.encode('8859', 'replace')
        else:
            strActual = str(actual)

        if expected is None:
            if actual is None:
                return
            else:
                raise AssertionError('Expected: None, actual: ' + strActual)

        if actual is None:
           raise AssertionError(1, 'Expected: ' + strExpected + ', actual: None')

        if (strExpected == strActual):
            return
    
        assert False, 'Expected: ' + strExpected + ', actual: ' + strActual

    def test_base(self):
        df = DupFinder()
        assert True, len(df.files) > 2

        print df.files


if __name__ == '__main__':
    print "testing"
    unittest.main()
    #run_tests()
    #print "Tests without exceptions"



