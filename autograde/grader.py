import unittest
import sys
import os

def check_file(f, Test):
    Test.student_file = f
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
        
def test(f, Test):
    realstdout = sys.stdout 
    sys.stdout = open('/dev/null', "w")
    Test.student_file = f
    Test.setUpClass()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    results = {}
    for test in suite._tests:
            r = unittest.TestResult()
            test.run(r)
            if r.errors:
                outcome = 0
            elif r.failures:
                outcome = 0
            else:
                outcome = Test.points(test._testMethodName[5:]) # skip "test_" prefix
            results[test._testMethodName] = outcome
    sys.stdout = realstdout
    return results

def anr(filename):
    return os.path.basename(filename).split('_')[1]

def scores(fs, Test):
    grades = []
    for f in fs:
        results = test(f, Test)
        score = sum(results.values())
        grades.append((anr(f), score))
    return sorted(grades)
