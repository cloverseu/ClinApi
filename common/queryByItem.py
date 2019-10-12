from model.projectModel import Project
from model.userModel import User
from model.fileModel import File
from model.taskModel import Task
from model.templateModel import Template
from model.db import db
from sqlalchemy import func, text


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
            print(i)
            print(self.data.get(i))
            if (self.data.get(i)):
                # 仅能有一个模糊查询
                print(str(i))
                if "ID" not in str(i):
                    like_key = 1
                filters[i] = self.data.get(i)
        # tasksInfo = Tasks.query.filter_by(**filters)
        # itemkey = list(self.data.keys())[0]
        # 查询item所在的model
        #db.session().query(models.TestItems, models.Test).join(models.Test, models.Test.id == models.TestItems.test_id)
        #联合多表查询:多个对应一个表很难，建议这部分数据库重复，建议先把创建的内容弄起来
        # a = Task.query.join(User,  Task.taskExecutorID == User.userID).filter(User.username=="user1").first()
        # print(66,a.taskID)
        q = None
        all_model = [Project, User, File, Task, Template]
        for i in all_model:
            #保证第一个字段一定在这个表里
            if item[0] in dir(i):
                if (like_key):
                    #属性作为参数传递i.i=>getattr()
                    for j in filters:
                        if "Time" in j:
                            # 时间的查询单独拿出来，只针对这个变量，其他变量需要修改
                            qsql =   "select * from project where to_char(project.\"projectCreatedTime\", 'YYYY-MM') like '"+filters[j]+"'"
                            print(qsql)
                            q = i.query.from_statement(text("select * from project where to_char(project.\"projectCreatedTime\", 'YYYY-MM') like '"+filters[j]+"'")).all()
                        else:
                            like_filters.append(getattr(i,j).like('%'+filters[j]+'%') if j is not None else "")
                    #非时间的条件
                    l = i.query.filter(*like_filters).all()
                    if q:
                        return list(set(l).intersection(set(q)))
                    else:
                        return l
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

