from model.trialModel import Trial
from model.userModel import User
from model.taskFilesModel import taskFiles
from model.tasksModel import Tasks



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
        #返回key-value不为空的值
        for i in item:
            if (self.data.get(i)):
                filters[i] = self.data.get(i)
        print(filters)
        # tasksInfo = Tasks.query.filter_by(**filters)
        # itemkey = list(self.data.keys())[0]
        # 查询item所在的model
        print(item)
        all_model = [Trial, User, taskFiles, Tasks]
        for i in all_model:
            if item[0] in dir(i):
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

