
# layer 0: Background Objects
# layer 1: Foreground Objects
# layer 2: Player Objects
# layer 3: Event Objects

# game world를 이용하여 map을 작성하고 main_state에 넘기도록 만들자.

objects = [[], []]


def add_object(o, layer): # 게임 월드에 객체 추가
    objects[layer].append(o)


def add_objects(l, layer): # 게임 월드에 객체들을 추가
    objects[layer] += l


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break


def clear():
    for o in all_objects():
        del o
    for l in objects:
        l.clear()


def destroy():
    clear()
    objects.clear()


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o # yield???