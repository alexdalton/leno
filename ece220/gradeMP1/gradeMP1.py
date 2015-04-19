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
          results.write("\n********** Test Input {0} **********\n".format(i))
          subprocess.call(["lc3sim -s testFiles/runtest{0} > testFiles/yourOut{0}".format(i)], shell=True)
          subprocess.call(["diff -b testFiles/yourOut{0} testFiles/ourOut{0} > testFiles/diff{0}".format(i)], 
                          shell=True)
          yourOut = open("testFiles/yourOut{0}".format(i), "r")
          ourOut  = open("testFiles/ourOut{0}".format(i), "r")
          ourSolution = {}
          yourSolution = {}

          missing_line = False
          incorrect_value = False

          for char in "@ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            yourSolution[char] = -1

          for line in ourOut:
            if re.match("[@ABCDEFGHIJKLMNOPQRSTUVWXYZ] \d", line):
              line = line.lstrip().rstrip()
              ourSolution[line[0]] = int(line[1:], base=16)

          for line in yourOut:
            if re.match("[@ABCDEFGHIJKLMNOPQRSTUVWXYZ] \d", line):
               line = line.lstrip().rstrip()
               try:
                 value = int(line[1:], base=16)
               except ValueError:
                 value = -2
                 incorrect_value = True
               yourSolution[line[0]] = value

          for char in "@ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if yourSolution[char] == -1:
              missing_line = True
            if yourSolution[char] != ourSolution[char] and yourSolution[char] != -1:
              incorrect_value = True

          if missing_line is False and incorrect_value is False:
            results.write("Test Passed!\n")
          if missing_line:
            results.write("Missing bins\n")
          if incorrect_value:
            results.write("Bin values incorrect\n")
              
          


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

    def runLateSub(self, results, deadline):
        late_results = subprocess.Popen(["bash", "/home/adalton2/leno/ece220/lateSub.sh",
                                         "-d", deadline], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE).communicate()
        results.write(late_results[0])
        if late_results[1]:
            results.write(late_results[1])

    def copyTestFiles(self, studentDir):
        subprocess.call(["cp", "-r", "/home/adalton2/leno/ece220/gradeMP1/testFiles/",
                         studentDir])

    def run(self):
        cwd = os.getcwd()
        for student in self.roster:
            studentDir = os.path.join(self.mpDirectory, string.rstrip(student, '\n'))
            os.chdir(studentDir)
            print("testing in " + os.getcwd())
            results = open("results.txt", "w")
            self.copyTestFiles(studentDir)

            self.runLateSub(results, "2015-01-28 22:00")

            self.testCompilation(results)
            self.testMP(results)

            results.close()

        os.chdir(cwd)

if __name__ == "__main__":
    roster, mpDirectory = getArgs()
    grader = autoGrader(roster, mpDirectory)
    grader.run()
