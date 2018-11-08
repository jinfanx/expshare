from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    '''
    模型基类
    '''

    id = models.AutoField(primary_key=True)
    #创建时间
    createdate = models.DateTimeField(verbose_name='创建时间')
    #更新时间
    updatedate = models.DateTimeField(verbose_name='更新时间')
    #创建人
    createuser = models.CharField(max_length=30,verbose_name='创建人')
    #更新人
    updateuser = models.CharField(max_length=30,verbose_name='更新人')

    class Meta:
        abstract = True


class CategoryModel(BaseModel):
    '''
    分类
    '''

    # 名称
    name = models.CharField(max_length=10,verbose_name='名称')
    # 访问量&热度
    viewnum = models.BigIntegerField(verbose_name='热度')

    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = u'分类'

class ExpModel(BaseModel):
    '''
    经验
    '''

    #分类
    category = models.ForeignKey(to='CategoryModel',to_field='id',on_delete=models.DO_NOTHING,verbose_name='分类')
    #关键字
    keywords = models.CharField(max_length=1000,verbose_name='关键字')
    #热度
    viewnum = models.BigIntegerField(verbose_name='热度')
    #状态 0-正常 1-待处理 2-处理中 3-停用
    state = models.IntegerField(default=0,verbose_name='状态')
    #问题
    problem = models.CharField(max_length=2000,verbose_name='问题')
    #原因
    reason = models.CharField(max_length=2000,verbose_name='原因')
    #解决方法
    resolve = models.TextField(verbose_name='解决方法')

    class Meta:
        verbose_name = u'经验'
        verbose_name_plural = u'经验'

    def __str__(self):
        return "{0}".format(self.problem)

#用户模型拓展-通过外键关联
class UserExtends(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=11,verbose_name='手机号')
    #职业 0-学生 1-职场人
    profession = models.IntegerField(verbose_name='职业')

#反馈-注册用户真对某条记录发起的反馈，包括错误反馈、有疑问等
class Feedback(BaseModel):
    share = models.ForeignKey(to='ExpModel',to_field='id',on_delete=models.CASCADE,verbose_name='问题')
    reason = models.TextField(max_length=2000,verbose_name='原因')
    is_resolved = models.BooleanField(default=False,verbose_name='已处理')
    # 状态 0-待处理 1-处理中 2-已完结
    state = models.IntegerField(default=0, verbose_name='状态')
    # 反馈类型 0-错误 1-有疑问
    type = models.IntegerField(default=0,verbose_name='类型')
    resolve_note = models.TextField(max_length=500,verbose_name='处理说明')

    class Meta:
        verbose_name = u'反馈'
        verbose_name_plural = u'反馈'

    def __str__(self):
        return "问题：{0}——理由：{1}".format(self.share,self.reason)

#点赞记录
class SharePraise(models.Model):
    id = models.AutoField(primary_key=True)
    shareid = models.IntegerField()
    userid = models.IntegerField()