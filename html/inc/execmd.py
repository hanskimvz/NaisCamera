import os, time, sys
import paramiko

print (sys.argv)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
try:
    ssh.connect('localhost', port=22, username='root', password='pass')
    t = True
except Exception as e:
    print (e)
    t = False
if not t:
    ssh.close()
    sys.exit()

stdin, stdout, stderr = ssh.exec_command(sys.argv[1])
stdin.close()
print (stdout.read().decode())

#  make tar file on device
# stdin, stdout, stderr = ssh.exec_command("cd /home; tar cvf home.tar bin/ html/ setting/")
# stdin.close()
# print (stdout.read().decode())

# sftp = ssh.open_sftp()
# for f in files:
#     sfname, dfname = f
#     print ( "%s => %s" %(sfname, dfname), end="")
#     print ("..", end="")
#     try:
#         x = sftp.get(sfname, dfname)
#     except Exception as e:
#         print (".......Fail")
#         print ("                          " +str(e))
        
#     else:
#         print ("..done", end="")

#     print ()


# sftp.close()

# stdin, stdout, stderr = ssh.exec_command("rm /home/home.tar")
# stdin.close()
# print (stdout.read().decode())



ssh.close()
