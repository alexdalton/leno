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
        self.due = "2015-03-18 22:00"

    def testMP(self, results):
          sierp = 0
          hex = 0
          printIm = 0
          square = 0
          drawHex = 0
          compare = []

          if os.path.exists("prog7"):

            subprocess.call(["timeout 10s ./prog7 1 0"], shell=True)

            try:
              if open("result.pgm", "r"):
                printIm = 10
            except IOError:
              printIm = 0

            x = subprocess.Popen(["compare", "-metric", "ae", "result.pgm", "/home/adalton2/leno/ece220/gradeMP7/goldoutput/sierpinski0.pgm", "output.pgm"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()
            try:
                compare.append(int(x[1]))
            except ValueError:
                compare.append(10000000)
            except IndexError:
                compare.append(10000000)

            subprocess.call(["timeout 10s ./prog7 1 1"], shell=True)
            x = subprocess.Popen(["compare", "-metric", "ae", "result.pgm", "/home/adalton2/leno/ece220/gradeMP7/goldoutput/sierpinski1.pgm", "output.pgm"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()
            try:
                compare.append(int(x[1]))
            except ValueError:
                compare.append(10000000)
            except IndexError:
                compare.append(10000000)

            subprocess.call(["timeout 10s ./prog7 1 2"], shell=True)
            x = subprocess.Popen(["compare", "-metric", "ae", "result.pgm", "/home/adalton2/leno/ece220/gradeMP7/goldoutput/sierpinski2.pgm", "output.pgm"], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate()
            try:
                compare.append(int(x[1]))
            except ValueError:
                compare.append(10000000)
            except IndexError:
                compare.append(10000000)

            subprocess.call(["timeout 10s ./prog7 2 1"], shell=True)
            x = subprocess.Popen(["compare", "-metric", "ae", "result.pgm", "/home/adalton2/leno/ece220/gradeMP7/goldoutput/hexflake1.pgm", "output.pgm"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()
            try:
                compare.append(int(x[1]))
            except ValueError:
                compare.append(10000000)
            except IndexError:
                compare.append(10000000)

            subprocess.call(["timeout 10s ./prog7 2 2"], shell=True)
            x = subprocess.Popen(["compare", "-metric", "ae", "result.pgm", "/home/adalton2/leno/ece220/gradeMP7/goldoutput/hexflake2.pgm", "output.pgm"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()
            try:
                compare.append(int(x[1]))
            except ValueError:
                compare.append(10000000)
            except IndexError:
                compare.append(10000000)

            subprocess.call(["timeout 10s ./prog7 3 2"], shell=True)
            x = subprocess.Popen(["compare", "-metric", "ae", "result.pgm", "/home/adalton2/leno/ece220/gradeMP7/goldoutput/square_tri2.pgm", "output.pgm"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()
            try:
                compare.append(int(x[1]))
            except ValueError:
                compare.append(10000000)
            except IndexError:
                compare.append(10000000)
    
            if compare[0] == 0:
                drawHex = 30
            elif compare[0] < 30:
                drawHex = 15

            if compare[1] == compare[2] == compare[3] == compare[4] == 0:
                sierp = 30
                hex = 10
            else:
                error1 = (compare[1] / 117504) * 100
                error2 = (compare[2] / 1057536) * 100
                sierp = max(0, 30 - 5 * max(error1, error2))
                error1 = (compare[3] / 117504) * 100
                error2 = (compare[4] / 1057536) * 100
                hex = max(0, 10 - 5 * max(error1, error2))

            if compare[5] == 0:
                square = 20
            print compare 
          results.write("******** Grading Results: ********\n")
          results.write("Sierpinski: {0}\n".format(sierp))
          results.write("drawHexagon: {0}\n".format(drawHex))
          results.write("hexaFlake: {0}\n".format(hex))
          results.write("printImage: {0}\n".format(printIm))
          results.write("challenge: {0}\n".format(square))
          total = sierp + hex + printIm + square + drawHex
          results.write("Total functionality points {0}/80\n".format(total))

    def testCompilation(self, results):
        subprocess.call(["rm", "-f", "prog7"])
        results.write("******** Compilation Results: ********\n")
        compile_results = subprocess.Popen(["gcc", "-o", "prog7", "prog7.c", "-lm"], stdout=subprocess.PIPE,
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
        subprocess.call(["cp", "-r", 
                         "/home/adalton2/leno/ece220/gradeMP{0}/testFiles/".format(self.mpNum),
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
