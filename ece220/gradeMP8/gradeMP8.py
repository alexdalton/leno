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
        self.due = "2015-04-08 22:00"

    def testMP(self, results):
        testFiles = ['testFiles/test1.txt', 'testFiles/test2.txt', 'testFiles/test3.txt']
        results.write("\n");
        i = 0
        findStartScores = []
        foundScore = False
        for test in testFiles:
            subprocess.call(["timeout 5s ./testMP8 {0} 0 > testFiles/findStart{1}".format(test, i)], shell=True)
            file = open("testFiles/findStart{0}".format(i), "r")
            contents = file.read()
            results.write(contents)
            contents = contents.split("Score:")
            if len(contents) > 1:
                foundScore = True
                findStartScores.append(int(contents[1])) 
            else:
                findStartScores.append(0)
                results.write("Test findStart on {0}\n    Score: 0\n")
            i = i + 1
        if foundScore:
          findStart = max(min(findStartScores), 0)
        else:
          findStart = 0
  
        i = 1
        printMazeScores = []
        for test in testFiles:
            subprocess.call(["timeout 5s ./testMP8 {0} 1 > testFiles/printMaze{1}".format(test, i)], shell=True)
            x = subprocess.Popen(["diff", "testFiles/printMaze{0}".format(i), test], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if x[0] == '':
               printMazeScores.append(5)
            else:
               printMazeScores.append(0)
            i = i + 1

        printMaze = max(min(printMazeScores), 0)

        i = 1
        DFSScores = []
        foundScore = False
        failedUnsolv = 0
        for test in testFiles:
            subprocess.call(["timeout 5s ./testMP8 {0} 2 > testFiles/solveMazeDFS{1}".format(test, i)], shell=True)
            file = open("testFiles/solveMazeDFS{0}".format(i), "r")
            contents = file.read()
            results.write(contents)
            contents = contents.split("Score:")
            if len(contents) > 1:
                foundScore = True
                if i == 3 and int(contents[1]) == 0:
                    failedUnsolv = 10
                    continue
                DFSScores.append(int(contents[1]))
            elif i == 3:
                results.write("Test solveMazeDFS on {0}\n    -10 points, failed unsolvable maze case\n    Score: 0\n".format(test))
                failedUnsolv = 10
            else:
                results.write("Test solveMazeDFS on {0}\n    Score: 0\n")
                DFSScores.append(0) 
                 

            i = i + 1
        if foundScore:
          solveMazeDFS = max(min(DFSScores) - failedUnsolv, 0)
        else:
          solveMazeDFS = 0

        i = 1
        BFSScores = []
        foundScore = False
        for test in testFiles:
            subprocess.call(["timeout 5s ./testMP8 {0} 4 > testFiles/solveMazeBFS{1}".format(test, i)], shell=True)
            file = open("testFiles/solveMazeBFS{0}".format(i), "r")
            contents = file.read()
            results.write(contents)
            contents = contents.split("Score:")
            if len(contents) > 1:
                foundScore = True
                BFSScores.append(int(contents[1])) 
            else:
                results.write("Test solveMazeBFS on {0}\n    Score: 0\n")
                BFSScores.append(0)

            i = i + 1
        if foundScore:
          solveMazeBFS = max(min(BFSScores), 0)
        else:
          solveMazeBFS = 0

        checkMazeScores = []
        i = 1
        for i in range(1,5):
            subprocess.call(["timeout 5s ./testMP8 testFiles/check{0}.txt 3 > testFiles/checkMaze{0}".format(i)], shell=True)
            file = open("testFiles/checkMaze{0}".format(i), "r")
            contents = file.read()
            results.write(contents)
            contents = contents.split("Score:")
            if len(contents) > 1:
                checkMazeScores.append(int(contents[1])) 
            else:
                results.write("Test checkMaze on {0}\n    Score: 0\n")

            i = i + 1
        checkMaze = sum(checkMazeScores)

        results.write("\nfindStart: {0}\n".format(findStart))
        results.write("printMaze: {0}\n".format(printMaze))
        results.write("solveMazeDFS: {0}\n".format(solveMazeDFS))
        results.write("checkMaze: {0}\n".format(checkMaze))
        results.write("solveMazeBFS: {0}\n".format(solveMazeBFS))
        results.write("Total: {0}/80\n".format(findStart + printMaze + solveMazeDFS + checkMaze + solveMazeBFS))
      
    def testCompilation(self, results):
        subprocess.call(["make", "clean"])
        results.write("******** Compilation Results: ********\n")
        compile_results = subprocess.Popen(["make", "test"], stdout=subprocess.PIPE,
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
        subprocess.call(["cp", "/home/adalton2/leno/ece220/gradeMP{0}/Makefile".format(self.mpNum),
                         studentDir])
        subprocess.call(["cp", "/home/adalton2/leno/ece220/gradeMP{0}/test.c".format(self.mpNum),
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
