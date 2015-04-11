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
        scores = []
        for i in range(1,4):
          results.write("\n********** Test Number {0} **********\n".format(i))

          subprocess.call(["timeout 5s ./mp4 testFiles/test{0} > testFiles/yourOut{0}".format(i)], shell=True)
          subprocess.call(["timeout 5s ./testFiles/compare testFiles/test{0} testFiles/yourOut{0} > testFiles/compare{0}".format(i)], 
                          shell=True)
          compare = open("testFiles/compare{0}".format(i), "r")
          contents = compare.read()
          compare.close()
          results.write(contents + '\n')
          try:
            value = float(contents.split()[3])
            lost = int(((value - 1) * 5))
          except ValueError as e:
            results.write("Value error: {0}\nTest failed\n".format(e))
            scores.append(80)
            continue
          except OverflowError as e:
            results.write("Overflow error: {0}\nTest failed\n".format(e))
            scores.append(80)
            continue
          if value <= 1.0:
            results.write("-0 points\n")
            scores.append(0)
          else:
            results.write("-{0} points\n".format(lost))
            scores.append(lost)
        results.write("\nFunctionality score {0}/80\n".format(80 - min(max(scores), 80) + self.challenge(results)))

    def challenge(self, results):
        results.write("\n********** Challenge **********\n")

        subprocess.call(["./mp4 testFiles/challenge > testFiles/challengeOut"], shell=True)
        subprocess.call(["./testFiles/compare testFiles/challenge testFiles/challengeOut > testFiles/challengeCompare"], 
                          shell=True)
        compare = open("testFiles/challengeCompare", "r")
        contents = compare.read()
        compare.close()
        results.write(contents + '\n')
        try:
          value = float(contents.split()[3])
        except ValueError:
          resultes.write("compare output malformed\n")
          return 0
        if value <= 1.0:
          results.write("Challenge Passed\n")
          return 20
        else:
          results.write("Challenge Failed\n")
          return 0
       
    
    def testCompilation(self, results):
        subprocess.call(["rm", "-f", "mp4", "*.o"])
        results.write("******** Compilation Results: ********\n")
        compile_results = subprocess.Popen(["gcc", "main.c", "-o", "mp4", "-lm"], stdout=subprocess.PIPE,
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
        subprocess.call(["cp", "-r", "/home/adalton2/leno/ece220/gradeMP4/testFiles/",
                         studentDir])

    def run(self):
        cwd = os.getcwd()
        for student in self.roster:
            studentDir = os.path.join(self.mpDirectory, string.rstrip(student, '\n'))
            os.chdir(studentDir)
            print("testing in " + os.getcwd())
            results = open("results.txt", "w")
            self.copyTestFiles(studentDir)

            self.runLateSub(results, "2015-02-22 22:00")

            self.testCompilation(results)
            self.testMP(results)

            results.close()

        os.chdir(cwd)

if __name__ == "__main__":
    roster, mpDirectory = getArgs()
    grader = autoGrader(roster, mpDirectory)
    grader.run()
