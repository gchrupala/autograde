import unittest
import sys
import os
import os.path
from numpy.testing import assert_allclose, assert_equal
import glob
import re

def get_name_test_vision(f):
    match = re.search('\)_[0-9]+_(.+)\.py', f)
    if match is not None:
        return match.group(1)
    else:
        return os.path.splitext(os.path.basename(f))[0]
    
def run_on_file(f, Test):
    "Run tests on file."
    Test.student_file = f
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)

    
def run_on_directory(directory, Test, get_name=get_name_test_vision, stream=sys.stdout, pattern="*.py"):
    "Run tests on directory."
    files = glob.glob(directory + "/" + pattern)
    for f in files:
        name = get_name(f)
        Test.student_file = f
        Test.setUpClass()
        suite = unittest.TestLoader().loadTestsFromTestCase(Test)
        tests = dict((test._testMethodName[5:], test) for test in suite._tests)
        test = tests.get(name)
        if test is not None:
            unittest.TextTestRunner(verbosity=2, stream=stream).run(test)
        
    
def score_file(f, Test):
    "Compute score on file."
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
# Backward compatibility
test = score_file

def score_directory(directory, Test, get_name=get_name_test_vision, pattern="*.py"):
    "Compute score on directory."
    realstdout = sys.stdout
    sys.stdout = open('/dev/null', "w")
    files = glob.glob(directory + "/" + pattern)
    results = {}
    for f in files:
        name = get_name(f)
        Test.student_file = f
        Test.setUpClass()
        suite = unittest.TestLoader().loadTestsFromTestCase(Test)

        tests = dict((test._testMethodName[5:], test) for test in suite._tests)
        test = tests.get(name)
        if test is not None:
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

def identity(x):
    return x

def check_strict(tester, function, inputs, post=identity):
    "Check whether outputs match exactly."
    for args in inputs:
        gold = tester.gold[function](*args)
        stud = tester.student[function](*args)
        assert_equal(post(gold), post(stud))

def check_close(tester, function, inputs, post=identity):
    "Check whether outputs (assumed to be numpy arrays) match approximately."
    for args in inputs:
        gold = tester.gold[function](*args)
        stud = tester.student[function](*args)
        assert_allclose(post(gold), post(stud))

def check_seq_close(tester, function, inputs, post=identity):
    "Check whether outputs (assumed to be tuples of numpy arrays) match approximately."
    for args in inputs:
        gold = tester.gold[function](*args)
        stud = tester.student[function](*args)
        for (a,b) in zip(gold, stud):
            assert_allclose(post(a), post(b))

def check_pos_close(tester, function, inputs, pos, post=identity):
    "Check whether outputs (assumed to be tuples of numpy arrays) match approximately at position pos."
    for args in inputs:
        gold = tester.gold[function](*args)
        stud = tester.student[function](*args)
        assert_allclose(post(gold[pos]), post(stud[pos]))
	
def check(tester, function, inputs):
    "Check whether outputs match. Tries to be too smart: use at own risk."
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
