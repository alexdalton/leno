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
        type = ["mult", "add", "sub", "all three", "invalid 1", "invalid 2", "div", "power"]
        for i in range(1,9):
          results.write("\n********** Test Input {0} {1} **********\n".format(i, type[i - 1]))

          subprocess.call(["lc3sim -s testFiles/runtest{0} > testFiles/yourOut{0}".format(i)], shell=True)
          subprocess.call(["diff -b testFiles/yourOut{0} testFiles/ourOut{0} > testFiles/diff{0}".format(i)], 
                          shell=True)
          yourOut = open("testFiles/yourOut{0}".format(i), "r")
          ourOut  = open("testFiles/ourOut{0}".format(i), "r")

          ourSolution = -1
          yourSolution = -1

          if i == 5 or i == 6:
            p = re.compile("Invalid Expression", re.IGNORECASE)
            flag = True
            for line in yourOut:
                if re.match(p, line):
                    results.write("Test Passed\n")
                    flag = False
                    break
            if flag:
                results.write("Test failed, invalid expression not printed\n")
          else:
            for line in ourOut:
              if re.search("R6=x", line):
                ourSolution = int(line.split()[6][4:], 16)
            for line in yourOut:
              if re.search("R6=x", line):
                try:
                  yourSolution = int(line.split()[6][4:], 16)
                except ValueError:
                  pass
            if ourSolution == yourSolution:
              results.write("Test passed\n")
            else:
              results.write("Test failed, incorrect R6 value\n")

    
    def testCompilation(self, results):
        subprocess.call(["rm", "-f", "*.sym", "*.obj"])
        results.write("******** Compilation Results: ********\n")
        compile_results = subprocess.Popen(["lc3as", "prog3.asm"], stdout=subprocess.PIPE,
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
        subprocess.call(["cp", "-r", "/home/adalton2/leno/ece220/gradeMP3/testFiles/",
                         studentDir])

    def run(self):
        cwd = os.getcwd()
        for student in self.roster:
            studentDir = os.path.join(self.mpDirectory, string.rstrip(student, '\n'))
            os.chdir(studentDir)
            print("testing in " + os.getcwd())
            results = open("results.txt", "w")
            self.copyTestFiles(studentDir)

            self.runLateSub(results, "2015-02-11 22:00")

            self.testCompilation(results)
            self.testMP(results)

            results.close()

        os.chdir(cwd)

if __name__ == "__main__":
    roster, mpDirectory = getArgs()
    grader = autoGrader(roster, mpDirectory)
    grader.run()
