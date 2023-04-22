import subprocess as sp
import pexpect
import re
import json
import time


SUBPROCESS_ENCODE = "shift-jis"

if __name__ == "__main__":
    with open("./config.json", "r", encoding="utf-8") as jf:
        config = json.load(jf)
    
    N = int(input("Number of times repeated:"))
    for i in range(N):

        # %format pre-process
        prd_com = []
        for com in config["stdin_list"]:
            prd_com.append(re.sub(r"%k",str(i+1), com))

        with sp.Popen(prd_com[0],shell=True, stdin=sp.PIPE) as proc:
                #output = proc.communicate(input=prd_com[1].encode("utf-8"))[0]
                #print(output.decode("utf-8"))
            prd_com.pop(0)
            for c in prd_com:
                while not proc.stdin.writable():
                        time.sleep(1e-6)
                proc.stdin.write(c.encode(SUBPROCESS_ENCODE))
                proc.stdin.write("\n".encode(SUBPROCESS_ENCODE))
                proc.stdin.flush()