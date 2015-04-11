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
    parser.add_option("-m", "--mp", dest="mpNum",
                      help="mp number")

    (options, args) = parser.parse_args()

    if options.mpdir is None or options.roster is None or options.mpNum is None:
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
    return (roster, mpDirectory, options.mpNum)


class autoGrader:
    def __init__(self, roster, mpDirectory, mpNum):
        self.roster = roster
        self.mpDirectory = mpDirectory
        self.mpNum = mpNum
        self.due = "2015-03-11 22:00"

    def testMP(self, results):
          radius = 0
          gaus = 0
          convolve = 0
          transf1 = 0
          transf2 = 0
          transf3 = 0
          transf4 = 0
          nearX = 0
          nearY = 0
          invert = 0
          dodge = 0
          gray = 0
          sketch = 0
          pixelate = 0
          subprocess.call(["timeout 10s ./gradetest > testOut"], shell=True)
          output = open("testOut", "r")

          results.write("******** Test Results: ********\n")
          for line in output:
              if re.match("getRadius correct", line):
                  radius = 5
              elif re.match("calculateGausFilter correct", line):
                  gaus = 10
              elif re.match("convolveImage correct", line):
                  convolve = 35
              elif re.match("nearestPixel Y value correct", line):
                  nearX = 5
              elif re.match("nearestPixel X value correct", line):
                  nearY = 5
              elif re.match("transformImage with shift transform correct", line):
                  transf1 = 5
              elif re.match("transformImage with scale transform correct", line):
                  transf2 = 5
              elif re.match("transformImage with rotation transform correct", line): 
                  transf3 = 5
              elif re.match("transformImage with general transform correct", line):
                  transf4 = 5
              elif re.match("convertToGray correct", line):
                  gray = 3
              elif re.match("invertImage correct", line):
                  invert = 5
              elif re.match("pixelate correct", line):
                  pixelate = 5
              elif re.match("colorDodge correct", line):
                  dodge = 5
              elif re.match("pencilSketch correct", line):
                  sketch = 2

          results.write("getRadius: {0}/5\n".format(radius))
          results.write("calculateGausFilter: {0}/10\n".format(gaus))
          results.write("convolveImage: {0}/35\n".format(convolve))
          results.write("transformImage 1: {0}/5\n".format(transf1))
          results.write("transformImage 2: {0}/5\n".format(transf2))
          results.write("transformImage 3: {0}/5\n".format(transf3))
          results.write("transformImage 4: {0}/5\n".format(transf4))
          results.write("nearest pixel X: {0}/5\n".format(nearX))
          results.write("nearest pixel Y: {0}/5\n".format(nearY))
          results.write("invertImage: {0}/5\n".format(invert))
          results.write("colorDodge: {0}/5\n".format(dodge))
          results.write("convertToGray: {0}/3\n".format(gray))
          results.write("pencilSketch: {0}/2\n".format(sketch))
          results.write("pixelate: {0}/5\n".format(pixelate))
          challenge = invert + dodge + gray + sketch + pixelate
          total = radius + gaus + convolve + transf1 + transf2 + transf3 + transf4 + nearX + nearY + challenge
          results.write("Total functionality points {0}/80\n".format(total))

    def testCompilation(self, results):
        subprocess.call(["rm", "-f", "mp" + self.mpNum, "functions.o"])
        results.write("******** Compilation Results: ********\n")
        compile_results = subprocess.Popen(["make", "gradetest"], stdout=subprocess.PIPE,
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
        subprocess.call(["cp", "/home/adalton2/leno/ece220/gradeMP{0}/testFiles/Makefile".format(self.mpNum),
                         studentDir])
        subprocess.call(["cp", "/home/adalton2/leno/ece220/gradeMP{0}/testFiles/gradetest.c".format(self.mpNum),
                         studentDir])
        subprocess.call(["cp", "/home/adalton2/leno/ece220/gradeMP{0}/testFiles/solution.o".format(self.mpNum),
                         studentDir])

    def run(self):
        cwd = os.getcwd()
        for student in self.roster:
            studentDir = os.path.join(self.mpDirectory, string.rstrip(student, '\n'))
            os.chdir(studentDir)
            print("testing in " + os.getcwd())
            results = open("results.txt", "w")
            self.copyTestFiles(studentDir)

            self.runLateSub(results, self.due)

            self.testCompilation(results)
            self.testMP(results)

            results.close()

        os.chdir(cwd)

if __name__ == "__main__":
    roster, mpDirectory, mpNum = getArgs()
    grader = autoGrader(roster, mpDirectory, mpNum)
    grader.run()
