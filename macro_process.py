import subprocess as sp
import pexpect
import re
import json
import time


SUBPROCESS_ENCODE = "shift-jis"

# 文字列から数式を抽出し、評価する関数
def evaluate_expression(expression, variables):
    # 正規表現パターンを定義します
    pattern = r'%\(?\d*[\+\-\*]?[ijk](?:[\+\-\*]\d*[ijk]?)*\)?'

    # 正規表現を使って数式を抽出します
    matches = re.findall(pattern, expression)
    # 抽出した数式を評価して代入します
    for match in matches:
        try:
            if len(match) > 1 and match[0] == "%":
                result = int(eval(match[1:], variables))
                expression = expression.replace(match, str(result))
        except:
            # 評価エラーが発生した場合、エラーメッセージを表示します
            print(f"Error evaluating expression: {match}")
            exit(1)

    return expression

if __name__ == "__main__":
    with open("./config.json", "r", encoding="utf-8") as jf:
        config = json.load(jf)
    
    # 正規表現パターン
    pattern = r'%\(?\d*[\+\-\*]?[ijk](?:[\+\-\*]\d*[ijk]?)*\)?'
    # 各変数の出現回数をカウント
    variable_count = {'i': 0, 'j': 0, 'k': 0}
    for s in config["stdin_list"]:
        # 正規表現を使用してパターンに合致する文字列を抽出
        matches = re.findall(pattern, s)
        for match in matches:
            if 'i' in match:
                variable_count['i'] += 1
            if 'j' in match:
                variable_count['j'] += 1
            if 'k' in match:
                variable_count['k'] += 1


    order = 0
    if variable_count['i'] > 0:
        L = int(input("Number of i-times repeated:"))
    else:
        L = 1
    if variable_count['j'] > 0:
        M = int(input("Number of j-times repeated:"))
    else:
        M = 1
    if variable_count['k'] > 0:
        N = int(input("Number of k-times repeated:"))
    else:
        N = 1
    if variable_count['i'] + variable_count['j'] + variable_count['k'] == 0:
        L = int(input("Number of repeated:"))



    for i in range(L):
        for j in range(M):
            for k in range(N):
                # %format pre-process
                variable_count = {'i': i, 'j': j, 'k': k}
                prd_com = []
                for com in config["stdin_list"]:
                    prd_com.append(evaluate_expression(com, variable_count))

                with sp.Popen(prd_com[0],shell=True, stdin=sp.PIPE) as proc:
                    prd_com.pop(0)
                    for c in prd_com:
                        while not proc.stdin.writable():
                                time.sleep(1e-6)
                        proc.stdin.write(c.encode(SUBPROCESS_ENCODE))
                        proc.stdin.write("\n".encode(SUBPROCESS_ENCODE))
                        proc.stdin.flush()