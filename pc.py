import threading
import time

import threading    # 导入threading模块
import queue      # 导入queue模块

""""
全部生产，全部消费
"""

# 生产者
class Producer(threading.Thread):# 定义生产者类

  def __init__(self,threadname):
    threading.Thread.__init__(self,name = threadname)

  def run(self):
    global que  # 声明queue为全局变量
    que.put(self.getName())  # 调用put方法将线程名添加到队列中
    print( self.getName(),'put ',self.getName(),' to queue')


# 消费者
class Consumer(threading.Thread):# 定义消费者类

  def __init__(self,threadname):
    threading.Thread.__init__(self,name = threadname)

  def run(self):
    global que
    print( self.getName(),'get ',que.get(),'from queue') #调用get方法获取队列中内容

que = queue.Queue()  # 生成队列对象
plist = []   # 生产者对象列表
clist = []   # 消费者对象列表
for i in range(10):
  p = Producer('Producer' + str(i))
  plist.append(p)   # 添加到生产者对象列表
for i in range(10):
  c = Consumer('Consumer' + str(i))
  clist.append(c)   # 添加到消费者对象列表
for i in plist:
  i.start()    # 运行生产者线程
  i.join()  # join() ? 主线程挂起，直到所有子线程运行完毕
for i in clist:
  i.start()    # 运行消费者线程
  i.join()


print('------------------------------------------------------------------------------------------------------')







'''

"""
生产后符合条件进行进行消费
"""

condition = threading.Condition() # condition对象在某些事件触发或者达到特定的条件后才处理数据
products = 0


# 生产者
class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global condition, products
        while True:
            if condition.acquire():
                if products < 10:
                    products += 1
                    print( "Producer(%s):deliver one, now products:%s" % (self.name, products))
                    condition.notify() # notify():通知其他线程，那些挂起的线程接到这个通知之后会开始运行
                else:
                    print( "Producer(%s):already 10, stop deliver, now products:%s" % (self.name, products))
                    condition.wait() #  wait():线程挂起
                condition.release()
                time.sleep(2)


# 消费者
class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global condition, products
        while True:
            if condition.acquire():
                if products > 1:
                    products -= 1
                    print("Consumer(%s):consume one, now products:%s" % (self.name, products))
                    condition.notify() # notify():通知其他线程，那些挂起的线程接到这个通知之后会开始运行
                else:
                    print( "Consumer(%s):only 1, stop consume, products:%s" % (self.name, products))
                    condition.wait() #  wait():线程挂起
                condition.release()
                time.sleep(2)


if __name__ == "__main__":
    for p in range(0, 2):
        p = Producer()
        p.start()

    for c in range(0, 10):
        c = Consumer()
        c.start()

'''