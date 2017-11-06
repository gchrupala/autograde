import unittest
import sys
import os
from numpy.testing import assert_allclose, assert_equal

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

def check(tester, function, inputs):
        for args in inputs:
            gold = tester.gold[function](*args)
            stud = tester.student[function](*args)

            try: # plain numpy arrays
                assert_allclose(gold, stud)
            except ValueError:
                 # sequences
                assert_equal(len(gold), len(stud))
                for i in range(len(gold)):
                    assert_allclose(gold[i], stud[i])
            except TypeError:
                # structured arrays
                try:
                    assert_equal(gold.dtype.names, stud.dtype.names)
                    try:
                        for col in gold.dtype.names:
                            try: # numeric field
                                assert_allclose(gold[col], stud[col])
                            except TypeError:
                                assert_equal(gold[col], stud[col])
                    except: TypeError
                    # string arrays
                    assert_equal(gold, stud)
                except AttributeError:
                    # something else
                    assert_equal(gold, stud)
