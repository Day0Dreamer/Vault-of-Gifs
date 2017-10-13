import subprocess


def gifsicle(lossy):
    cmdline = 'gifsicle.exe ' \
              '-O3 --lossy={} -no-extensions -o asd{}.gif --use-colormap table.txt ' \
              '"C:\Python\Vault_Of_Gifs\SteffonDiggsEmoji02280x28030FPS.gif"'.format(lossy, lossy)
    p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        else:
            output = line.decode("utf-8")
            print(output.strip())

for i in range(20, 150):
    gifsicle(i)
