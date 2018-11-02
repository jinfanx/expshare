from django.db import models

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