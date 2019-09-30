from model.projectModel import Project
from model.userModel import User
from model.fileModel import File
from model.taskModel import Task
from model.templateModel import Template
from model.db import db



class QueryConductor(object):



    def __init__(self, data, start=None, end=None):
        self.data = data
        self.start = start
        self.end = end


    def queryProcess(self):
        '''
                单一元素的查询：
                 (1)元素仅在parser.add_argument
                 (2) 仅为单表
                 (3)支持多个条件,但仅仅为等式
        '''

        # data_trial_id = data.get('taskID')
        # print(list(data.keys())[0])

        #返回所有的parser.add_argument对应的key值
        item = list(self.data.keys())

        filters = {}
        like_filters = []
        #返回key-value不为空的值
        like_key = None
        for i in item:
            if (self.data.get(i)):
                # 仅能有一个模糊查询
                if "ID" not in str(i):
                    like_key = 1
                filters[i] = self.data.get(i)

        print(filters)
        # tasksInfo = Tasks.query.filter_by(**filters)
        # itemkey = list(self.data.keys())[0]
        # 查询item所在的model
        #db.session().query(models.TestItems, models.Test).join(models.Test, models.Test.id == models.TestItems.test_id)
        #联合多表查询:多个对应一个表很难，建议这部分数据库重复，建议先把创建的内容弄起来
        # a = Task.query.join(User,  Task.taskExecutorID == User.userID).filter(User.username=="user1").first()
        # print(66,a.taskID)
        print(item)
        all_model = [Project, User, File, Task, Template]
        for i in all_model:
            #保证第一个字段一定在这个表里
            if item[0] in dir(i):
                if (like_key):
                    #属性作为参数传递i.i=>getattr()
                    for j in filters:
                        like_filters.append(getattr(i,j).like(filters[j]) if j is not None else "")
                    print(like_filters)
                    return i.query.filter(*like_filters).all()
                else:
                    return i.query.filter_by(**filters)
        # try:
        #
        # #构造查询项
        #     # filters = {item: self.data.get(item)}
        #     print(filters)
        #     #tasksInfo = Tasks.query.filter_by(**filters)
        #     #itemkey = list(self.data.keys())[0]
        #     #查询item所在的model
        #     all_model = [Trial, User, taskFiles, Tasks]
        #     for i in all_model:
        #         if item in dir(i):
        #             return i.query.filter_by(**filters)
        # except:
        #     return None
        #

    def queryInterval(self, item, start=None, end=None):
        '''
               用于区间的查询
        '''
        # all_model = [Trial, User, taskFiles, Tasks]
        # for i in all_model:
        #     if item in dir(i):
        #          i[item] = item
        # filters = {}
        # filters
        # if(self.start)
        # # filters = {
        # #     User.name == ‘fengyao’,
        # # User.age > 25
        # # }
        # User.query.filter(*filters).first()
    # # data_trial_id = data.get('taskID')
    # # print(list(data.keys())[0])
    #
    # # 返回所有的parser.add_argument对应的key值
    # item = list(self.data.keys())
    #
    # filters = {}
    # # 返回key-value不为空的值
    # for i in item:
    #     if (self.data.get(i)):
    #         filters[i] = self.data.get(i)
    # print(filters)
    # # tasksInfo = Tasks.query.filter_by(**filters)
    # # itemkey = list(self.data.keys())[0]
    # # 查询item所在的model
    # print(item)
    # all_model = [Trial, User, taskFiles, Tasks]
    # for i in all_model:
    #     if item[0] in dir(i):
    #         return i.query.filter_by(**filters)
    #         # try:
    #         #
    #         # #构造查询项
    #         #     # filters = {item: self.data.get(item)}
    #         #     print(filters)
    #         #     #tasksInfo = Tasks.query.filter_by(**filters)
    #         #     #itemkey = list(self.data.keys())[0]
    #         #     #查询item所在的model
    #         #     all_model = [Trial, User, taskFiles, Tasks]
    #         #     for i in all_model:
    #         #         if item in dir(i):
    #         #             return i.query.filter_by(**filters)
    #         # except:
    #         #     return None
    #         #

