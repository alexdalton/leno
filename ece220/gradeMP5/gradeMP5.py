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
          results.write("\n********** Test rootbound **********\n")
          subprocess.call(["timeout 5s ./mp5 testFiles/gradeOne > testFiles/yourOut1"], shell=True)
          contents = open("testFiles/yourOut1", "r").read()
          p = re.compile("the polynomial has no roots", re.IGNORECASE)
          q = re.compile("no roots found", re.IGNORECASE)
          r = re.compile("root found", re.IGNORECASE)
          if re.match(r, contents):
            results.write("Found a root when there should be none\nTest Failed\n")
          elif re.match(q, contents):
            results.write("Printed wrong message: may not have used rootbound correctly\nTest Failed\n")
          elif re.match(p, contents):
            results.write("Test Passed\n")
          else:
            results.write("Test Failed\n")
          
          results.write("\n********** Test newrfind **********\n")
          subprocess.call(["timeout 5s ./mp5 testFiles/gradeTwo > testFiles/yourOut2"], shell=True)
          contents = open("testFiles/yourOut2", "r")
          count = 0
          correct = 0
          p = re.compile("6.000000")
          for line in contents:
            if re.match(r, line):
                count = count + 1
                try:
                    value = float(line.split(":")[1])
                except ValueError:
                    continue
                if value == 6.0:
                    correct = correct + 1
          if correct == count and count >= 7:
            results.write("Test Passed\n")
          else:
            results.write("Test Failed\n")
          


    def testCompilation(self, results):
        subprocess.call(["rm", "-f", "mp5", "*.o"])
        results.write("******** Compilation Results: ********\n")
        compile_results = subprocess.Popen(["gcc", "mp5.c", "-o", "mp5", "-lm"], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE).communicate()
        if compile_results[1]:
            results.write("Compile Errors\n")
            results.write(compile_results[1])
            return False
        results.write("No compilation errors\n")
        return True

    def runLateSub(self, results, deadline):
        late_results = subprocess.Popen(["bash", "/home/adalton2/leno/ece220/lateSub.sh",
                                         "-d", deadline], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE).communicate()
        results.write(late_results[0])
        if late_results[1]:
            results.write(late_results[1])

    def copyTestFiles(self, studentDir):
        subprocess.call(["cp", "-r", "/home/adalton2/leno/ece220/gradeMP5/testFiles/",
                         studentDir])

    def run(self):
        cwd = os.getcwd()
        for student in self.roster:
            studentDir = os.path.join(self.mpDirectory, string.rstrip(student, '\n'))
            os.chdir(studentDir)
            print("testing in " + os.getcwd())
            results = open("results.txt", "w")
            self.copyTestFiles(studentDir)

            self.runLateSub(results, "2015-03-04 22:00")

            self.testCompilation(results)
            self.testMP(results)

            results.close()

        os.chdir(cwd)

if __name__ == "__main__":
    roster, mpDirectory = getArgs()
    grader = autoGrader(roster, mpDirectory)
    grader.run()
