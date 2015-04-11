import subprocess
import os
import string
import re
from optparse import OptionParser

def getArgs():
    parser = OptionParser()
    parser.add_option("-b", "--mpdir", dest="mpdir",
                      help="directory of pulled student MPs")
    parser.add_option("-r", "--roster", dest="roster",
                      help="student roster file", metavar="FILE")

    (options, args) = parser.parse_args()

    if options.mpdir is None or options.roster is None:
        parser.print_help()
        exit(1)

    mpDirectory = os.path.abspath(options.mpdir)

    if not os.path.exists(mpDirectory):
        print("{0} does not exist".format(mpDirectory))
        exit(1)

    try:
        rosterPath = os.path.abspath(options.roster)
        roster = open(rosterPath, "r")
    except IOError as e:
        print("I/O error({0}): {1} {2}".format(e.errno, rosterPath, e.strerror))
        exit(1)
    return (roster, mpDirectory)


class autoGrader:
    def __init__(self, roster, mpDirectory):
        self.roster = roster
        self.mpDirectory = mpDirectory

    def testMP(self, results):
        tests = [2, 5, 31]
        for test in tests:
          results.write("\n********** Test Input x = {0} **********\n".format(test))
          subprocess.call(["lc3sim -s testFiles/runtest{0} > testFiles/yourOut{0}".format(test)], shell=True)
          yourOut = open("testFiles/yourOut{0}".format(test), "r")
          ourSolution = {}
          for i in range(1, test):
            if i <= test - i:
              ourSolution[(i, test - i)] = 1
          testPassed = True
          for line in yourOut:
            items= line.split()
            val1 = -1
            val2 = -1
            try:
              val1 = int(items[0], 16)
              val2 = int(items[1], 16)
            except ValueError:
              continue
            except IndexError:
              continue
            if ourSolution[(val1, val2)] == 1:
              ourSolution[(val1, val2)] = 0
            else:
               testPassed = False
               break
          if testPassed:
            results.write("Test passed\n")
          else:
            results.write("Test failed\n")


 
    def testCompilation(self, results):
        subprocess.call(["rm", "-f", "*.sym", "*.obj"])
        results.write("******** Compilation Results: ********\n")
        compile_results = subprocess.Popen(["lc3as", "prog1.asm"], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE).communicate()
        if compile_results[1]:
            results.write("Compile Errors\n")
            results.write(compile_results[1])
            return False
        results.write("No compilation errors\n")
        return True


    def copyTestFiles(self, studentDir):
        subprocess.call(["cp", "-r", "/home/adalton2/leno/ece220/gradeMidterm1/testFiles/",
                         studentDir])


    def run(self):
        cwd = os.getcwd()
        for student in self.roster:
            studentDir = os.path.join(self.mpDirectory, string.rstrip(student, '\n'), "Problem1")
            os.chdir(studentDir)
            print("testing in " + os.getcwd())
            results = open("results.txt", "w")
            self.copyTestFiles(studentDir)


            self.testCompilation(results)
            self.testMP(results)

            results.close()

        os.chdir(cwd)

if __name__ == "__main__":
    roster, mpDirectory = getArgs()
    grader = autoGrader(roster, mpDirectory)
    grader.run()
