#  coding:utf-8
'''
2013-9-17  XTH
'''
import sys
import copy


def setglobalvar():   # 重置所有变量
    global max_sum, now_sum, min_x, min_y, num, visited, pointgroup, answermatrix
    max_sum = 0
    now_sum = 0
    min_x = 0
    min_y = 0
    num = []
    visited = {}
    pointgroup = []
    answermatrix = {}


def maxsum_h(num, n1, n2):    # 水平上相连
    global answermatrix
    line = [0]*n2
    max_sum = 0     # 最大和
    now_sum = 0     # 当前和
    for l in range(0, n2):
        for i in range(0, n1):
            for j in range(i, n1):
                visited = {}
                for k in range(0 + l, n2 + l):
                    tempk = k
                    k = k % n2
                    line[k] += num[j][k]
                    if now_sum < 0:
                        visited = {}
                        now_sum = 0
                    now_sum += line[k]
                    for q in range(i, j + 1):
                        visited[q, tempk] = 1
                    if now_sum > max_sum:
                        answermatrix = copy.deepcopy(visited)
                        max_sum = now_sum
                now_sum = 0
            now_sum = 0
            line = [0]*n2
    return max_sum


def maxsum_v(num, n1, n2):    # 垂直上相连
    global answermatrix
    line = [0]*n2
    max_sum = 0     # 最大和
    now_sum = 0     # 当前和
    for l in range(0, n1):
        for i in range(0, n1):
            for j in range(i + l, n1 + l):
                tempj = j
                visited = {}
                for k in range(0, n2):
                    j = j % n1
                    line[k] += num[j][k]
                    if now_sum < 0:
                        visited = {}
                        now_sum = 0
                    now_sum += line[k]
                    if tempj >= n1:
                        for q in range(i + 1, tempj + 1):
                            visited[q, k] = 1
                    else:
                        for q in range(i, tempj + 1):
                            visited[q, k] = 1
                    if now_sum > max_sum:
                        answermatrix = copy.deepcopy(visited)
                        max_sum = now_sum
                now_sum = 0
            now_sum = 0
            line = [0]*n2
    return max_sum


def maxsum(num, n1, n2):   # 最普通的情况
    global answermatrix
    line = [0]*n2
    max_sum = 0     # 最大和
    now_sum = 0     # 当前和
    for i in range(0, n1):
        for j in range(i, n1):
            visited = {}
            for k in range(0, n2):
                line[k] += num[j][k]
                if now_sum < 0:
                    visited = {}
                    now_sum = 0
                now_sum += line[k]
                for q in range(i, j + 1):
                    visited[q, k] = 1
                if now_sum > max_sum:
                    answermatrix = copy.deepcopy(visited)
                    max_sum = now_sum
            now_sum = 0
        now_sum = 0
        line = [0]*n2
    return max_sum


def maxsum_vh(num, n1, n2):   # 连通
    global answermatrix
    line = [0]*n2
    max_sum = 0     # 最大和
    now_sum = 0     # 当前和
    for l1 in range(0, n1):
        for l2 in range(0, n2):
            for i in range(0, n1):
                for j in range(i + l1, n1 + l1):
                    tempj = j
                    visited = {}
                    for k in range(0 + l2, n2 + l2):
                        tempk = k
                        j = j % n1
                        k = k % n2
                        line[k] += num[j][k]
                        if now_sum < 0:
                            visited = {}
                            now_sum = 0
                        now_sum += line[k]
                        if tempj >= n1:
                            for q in range(i + 1, tempj + 1):
                                visited[q, tempk] = 1
                        else:
                            for q in range(i, tempj + 1):
                                visited[q, tempk] = 1
                        if now_sum > max_sum:
                            answermatrix = copy.deepcopy(visited)
                            max_sum = now_sum
                    now_sum = 0
                now_sum = 0
                line = [0]*n2
    return max_sum


def walkthrough(x, y, num, tempmax):     # 递归找连通的最大值，贪心法，每次选择所有联通格子中最大的那个。
    global max_sum, visited, pointgroup, min_x, min_y, answermatrix
    if max_sum < tempmax:
        max_sum = tempmax
        answermatrix = copy.deepcopy(visited)
    for i in [[0, -1], [1, 0], [0, 1], [-1, 0]]:
        if x + i[0] >= min_x and x + i[0] < n1 and y + i[1] >= min_y and y + i[1] < n2 and visited[(x + i[0]) % n1, (y + i[1]) % n2] == 0 and [(x + i[0]) % n1, (y + i[1]) % n2, num[(x + i[0]) % n1][(y + i[1]) % n2]] not in pointgroup:
            pointgroup.append([(x + i[0]) % n1, (y + i[1]) % n2, num[(x + i[0]) % n1][(y + i[1]) % n2]])
    pointgroup = sorted(pointgroup, key=lambda x: x[2])
    if pointgroup == []:
        return
    temptarget = [pointgroup.pop()]
    while pointgroup and pointgroup[-1][2] == temptarget[0][2]:     # 这里是重点，如果有一样大的格子，就要分别递归。
        temptarget.append(pointgroup.pop())
    for i in temptarget:
        if tempmax + i[2] > 0:   # 剪枝
            visited[i[0], i[1]] = 1
            walkthrough(i[0], i[1], num, tempmax + i[2])
            visited[i[0], i[1]] = 0


def maxsum_a(num, n1, n2):    # 连通
    global min_x, min_y, max_sum, visited
    min_x = 0
    min_y = 0
    max_sum = 0
    now_sum = 0
    startpointx = []
    startpointy = []
    pointgroup = []
    for i in range(0, n1):
        for j in range(0, n2):
            visited[i, j] = 0
    for i in range(0, n1):
        for j in range(0, n2):
            if num[i][j] > 0:
                startpointx.append(i)
                startpointy.append(j)
    for pointx in startpointx:
        pointy = startpointy.pop()
        for i in range(0, n1):
            for j in range(0, n2):
                visited[i, j] = 0
        visited[pointx,  pointy] = 1
        visited[pointx,  pointy] = 1
        walkthrough(pointx, pointy, num, num[pointx][pointy])
    return max_sum


def maxsum_vha(num, n1, n2):    # 轮胎+连通
    global min_x, min_y, max_sum, visited
    min_x = -n1
    min_y = -n2
    max_sum = 0
    now_sum = 0
    startpointx = []
    startpointy = []
    pointgroup = []
    for i in range(0, n1):
        for j in range(0, n2):
            visited[i, j] = 0
            if num[i][j] > 0:
                startpointx.append(i)
                startpointy.append(j)
    startpointx.reverse()
    for pointx in startpointx:
        pointy = startpointy.pop()
        for i in range(0, n1):
            for j in range(0, n2):
                visited[i, j] = 0
        visited[pointx,  pointy] = 1
        walkthrough(pointx, pointy, num, num[pointx][pointy])
    return max_sum


def main():
    setglobalvar()
    global n1, n2
    max_sum = 0
    V = H = A = False
    if "\\v" in sys.argv[1:]:
        V = True
    if "\\h" in sys.argv[1:]:
        H = True
    if "\\a" in sys.argv[1:]:
        A = True
    filename = sys.argv[-1]
    try:
        f = open(filename, "r")
    except:
        raise IOError("ERROR:can't open the file")
    try:
        line = f.readline()
        line = line.strip('\n').strip(',')
        n1 = int(line)
        line = f.readline()
        line = line.strip('\n').strip(',')
        n2 = int(line)
        num = [[]] * int(n1)
        for i in range(0, int(n1)):
            line = f.readline()
            line = line.strip('\n')
            if len(line.split(",")) != n2:
                raise ValueError("ERROR:the format of file is wrong")
            num[i] = line.split(",")
        num = [[int(x) for x in inner] for inner in num]
    except:
        raise ValueError("ERROR:the format of file is wrong")
    if not V and not H and A:    # 连通
        max_sum = maxsum_a(num, n1, n2)
    elif V and not H and not A:  # 水平上相连
        max_sum = maxsum_v(num, n1, n2)
    elif not V and H and not A:  # 垂直上相连
        max_sum = maxsum_h(num, n1, n2)
    elif V and H and not A:  # 水平垂直上相连
        max_sum = maxsum_vh(num, n1, n2)
    elif V and H and A:  # 水平垂直上相连连通
        max_sum = maxsum_vha(num, n1, n2)
    else:  # 普通
        max_sum = maxsum(num, n1, n2)
    return max_sum, num, answermatrix


if __name__ == '__main__':
    print main()
