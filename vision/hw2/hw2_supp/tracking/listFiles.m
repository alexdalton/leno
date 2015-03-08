function filelist = listFiles(targetDir);
%lists all files in a directory in a cell array
cd(targetDir);
root = dir;
path = pwd;
[m n] = size(root);
count = 1;

for i=3:m
    if root(i).isdir == 0
        file = sprintf('%s\\%s',path,root(i).name);
        filelist{count} = file;
        count = count + 1;
    end
end
%this is only for convenience:

