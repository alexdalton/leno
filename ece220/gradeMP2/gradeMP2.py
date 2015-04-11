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
        for i in range(1,7):
          if i < 5:
            results.write("\n********** Test Input {0} **********\n".format(i))
          elif i == 5:
            results.write("\n********** Challenge 1 **********\n")
          elif i == 6:
            results.write("\n********** Challenge 2 **********\n")


          subprocess.call(["lc3sim -s testFiles/runtest{0} > testFiles/yourOut{0}".format(i)], shell=True)
          subprocess.call(["diff -b testFiles/yourOut{0} testFiles/ourOut{0} > testFiles/diff{0}".format(i)], 
                          shell=True)
          yourOut = open("testFiles/yourOut{0}".format(i), "r")
          ourOut  = open("testFiles/ourOut{0}".format(i), "r")

          if i != 6:
            ourSolution = []
            yourSolution = []

            for line in ourOut:
              if re.match("4FF8|5004", line):
                memoryContents = line[5:].split()
                for value in memoryContents:
                  try:
                      ourSolution.append(int(value, 16))
                  except ValueError:
                      continue

            for line in yourOut:
              if re.match("4FF8|5004", line):
                memoryContents = line[5:].split()
                for value in memoryContents:
                  try:
                    yourSolution.append(int(value, 16))
                  except ValueError:
                    continue

            if ourSolution == yourSolution:
              results.write("Test Passed\n")
            else:
              results.write("Memory does not match solution\n")
          else:
            p = re.compile("Error invalid input", re.IGNORECASE)
            for line in yourOut:
              if re.match(p, line):
                results.write("Test Passed\n")
                return
            results.write("Test Failed\n")

    
    def testCompilation(self, results):
        subprocess.call(["rm", "-f", "*.sym", "*.obj"])
        results.write("******** Compilation Results: ********\n")
        compile_results = subprocess.Popen(["lc3as", "prog2.asm"], stdout=subprocess.PIPE,
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
        subprocess.call(["cp", "-r", "/home/adalton2/leno/ece220/gradeMP2/testFiles/",
                         studentDir])

    def run(self):
        cwd = os.getcwd()
        for student in self.roster:
            studentDir = os.path.join(self.mpDirectory, string.rstrip(student, '\n'))
            os.chdir(studentDir)
            print("testing in " + os.getcwd())
            results = open("results.txt", "w")
            self.copyTestFiles(studentDir)

            self.runLateSub(results, "2015-02-04 22:00")

            self.testCompilation(results)
            self.testMP(results)

            results.close()

        os.chdir(cwd)

if __name__ == "__main__":
    roster, mpDirectory = getArgs()
    grader = autoGrader(roster, mpDirectory)
    grader.run()
